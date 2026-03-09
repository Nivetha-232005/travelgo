from __future__ import annotations

import importlib
import os
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List

from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


AWS_REGION = "ap-south-1"


def _is_truthy(value: str | None) -> bool:
	return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _has_value(value: str | None) -> bool:
	return bool(str(value or "").strip())


def _build_dynamodb_resource() -> Any:
	"""Create a DynamoDB resource only when endpoint/credentials are configured."""
	endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL")
	region_name = os.getenv("AWS_REGION", AWS_REGION)

	# If using a custom endpoint (for example local DynamoDB), allow explicit setup.
	if endpoint_url:
		kwargs: Dict[str, Any] = {
			"service_name": "dynamodb",
			"region_name": region_name,
			"endpoint_url": endpoint_url,
		}
		if os.getenv("AWS_ACCESS_KEY_ID"):
			kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID")
		if os.getenv("AWS_SECRET_ACCESS_KEY"):
			kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY")
		if os.getenv("AWS_SESSION_TOKEN"):
			kwargs["aws_session_token"] = os.getenv("AWS_SESSION_TOKEN")
		return boto3.resource(**kwargs)

	# For real AWS, only auto-enable when credential sources are configured.
	if _has_value(os.getenv("AWS_PROFILE")) or (
		os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY")
	):
		return boto3.resource("dynamodb", region_name=region_name)

	return None


def _to_dynamo(value: Any) -> Any:
	if isinstance(value, dict):
		return {key: _to_dynamo(val) for key, val in value.items()}
	if isinstance(value, list):
		return [_to_dynamo(item) for item in value]
	if isinstance(value, datetime):
		return value.isoformat()
	if isinstance(value, bool):
		return value
	if isinstance(value, float):
		return Decimal(str(value))
	if isinstance(value, int):
		return Decimal(value)
	return value


def _from_dynamo(value: Any) -> Any:
	if isinstance(value, dict):
		return {key: _from_dynamo(val) for key, val in value.items()}
	if isinstance(value, list):
		return [_from_dynamo(item) for item in value]
	if isinstance(value, Decimal):
		return int(value) if value % 1 == 0 else float(value)
	return value


def _matches_query(item: Dict[str, Any], query: Dict[str, Any]) -> bool:
	for key, expected in (query or {}).items():
		actual = item.get(key)

		if isinstance(expected, dict) and "$regex" in expected:
			import re

			regex = expected.get("$regex", "")
			options = expected.get("$options", "")
			flags = re.IGNORECASE if "i" in str(options).lower() else 0
			if actual is None or re.search(regex, str(actual), flags) is None:
				return False
			continue

		if actual != expected:
			return False

	return True


class DynamoCollection:
	def __init__(self, table: Any, table_name: str):
		self.table = table
		self.table_name = table_name
		self._use_local_store = False
		self._local_items: List[Dict[str, Any]] = []

	def _can_use_remote(self) -> bool:
		if self._use_local_store:
			return False
		return self.table is not None

	def _switch_to_local_store(self) -> None:
		self._use_local_store = True

	def _local_insert(self, item: Dict[str, Any]) -> Dict[str, Any]:
		self._local_items.append(dict(item))
		return {"acknowledged": True}

	def insert_one(self, document: Dict[str, Any]) -> Dict[str, Any]:
		item = dict(document)

		# Ensure expected key exists for collections that need one.
		if self.table_name == "plans" and "plan_id" not in item:
			item["plan_id"] = str(uuid.uuid4())
		if self.table_name == "bookings" and "booking_id" not in item:
			item["booking_id"] = str(uuid.uuid4())
		if self.table_name in {"hotels", "flights", "vehicles", "reviews", "wishlist"} and "id" not in item:
			item["id"] = str(uuid.uuid4())

		if not self._can_use_remote():
			return self._local_insert(item)

		try:
			self.table.put_item(Item=_to_dynamo(item))
			return {"acknowledged": True}
		except (NoCredentialsError, BotoCoreError, ClientError):
			self._switch_to_local_store()
			return self._local_insert(item)

	def insert_many(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
		for document in documents:
			self.insert_one(document)
		return {"acknowledged": True, "inserted_count": len(documents)}

	def find(self, query: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
		if not self._can_use_remote():
			items = [dict(item) for item in self._local_items]
			if not query:
				return items
			return [item for item in items if _matches_query(item, query)]

		items: List[Dict[str, Any]] = []
		scan_kwargs: Dict[str, Any] = {}

		try:
			while True:
				response = self.table.scan(**scan_kwargs)
				items.extend(_from_dynamo(item) for item in response.get("Items", []))

				if "LastEvaluatedKey" not in response:
					break

				scan_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
		except (NoCredentialsError, BotoCoreError, ClientError):
			self._switch_to_local_store()
			items = [dict(item) for item in self._local_items]

		if not query:
			return items

		return [item for item in items if _matches_query(item, query)]

	def find_one(self, query: Dict[str, Any]) -> Dict[str, Any] | None:
		results = self.find(query)
		return results[0] if results else None

	def count_documents(self, query: Dict[str, Any]) -> int:
		return len(self.find(query))


class DynamoDatabase:
	def __init__(self, dynamodb_resource: Any):
		self.dynamodb_resource = dynamodb_resource
		self._cache: Dict[str, DynamoCollection] = {}

	def __getitem__(self, collection_name: str) -> DynamoCollection:
		if collection_name not in self._cache:
			table = self.dynamodb_resource.Table(collection_name) if self.dynamodb_resource else None
			self._cache[collection_name] = DynamoCollection(table, collection_name)
		return self._cache[collection_name]


try:
	boto3 = importlib.import_module("boto3")
	dynamodb = _build_dynamodb_resource()
except ModuleNotFoundError as exc:
	raise RuntimeError("boto3 is required. Install it with: pip install boto3") from exc
except Exception:
	# Fall back to local in-memory collections when AWS is not configured.
	dynamodb = None

db = DynamoDatabase(dynamodb)

users_collection = db["users"]
bookings_collection = db["bookings"]
plans_collection = db["plans"]