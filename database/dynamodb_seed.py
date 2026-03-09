from __future__ import annotations

import uuid
import importlib
import os
from decimal import Decimal
from typing import Any, Dict, List


def get_seed_plans_data() -> List[Dict[str, Any]]:
    """Return the same TravelGo plans currently seeded in MongoDB."""
    return [
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Parisian Romance",
            "destination": "Paris, France",
            "source": "Any City",
            "duration": "5 Days / 4 Nights",
            "price": 1200,
            "category": "culture",
            "budget": "premium",
            "max_travelers": 6,
            "rating": 4.9,
            "icon": "🗼",
            "image_url": "https://images.unsplash.com/photo-1431274172761-fca41d930114?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Eiffel Tower", "Louvre Museum", "Seine River Cruise", "Montmartre"],
            "includes": ["Hotel", "Breakfast", "City Tour", "Airport Transfer"],
            "image_emoji": "🇫🇷"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Tropical Bali Escape",
            "destination": "Bali, Indonesia",
            "source": "Any City",
            "duration": "7 Days / 6 Nights",
            "price": 950,
            "category": "beach",
            "budget": "moderate",
            "max_travelers": 8,
            "rating": 4.8,
            "icon": "🏝️",
            "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Ubud Terraces", "Tanah Lot Temple", "Kuta Beach", "Monkey Forest"],
            "includes": ["Resort Stay", "All Meals", "Spa Treatment", "Guided Tour"],
            "image_emoji": "🌴"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Tokyo Adventure",
            "destination": "Tokyo, Japan",
            "source": "Any City",
            "duration": "6 Days / 5 Nights",
            "price": 1500,
            "category": "culture",
            "budget": "premium",
            "max_travelers": 4,
            "rating": 4.7,
            "icon": "🎌",
            "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Shibuya Crossing", "Mt. Fuji Day Trip", "Akihabara", "Tsukiji Market"],
            "includes": ["Hotel", "Breakfast", "JR Rail Pass", "Airport Transfer"],
            "image_emoji": "🇯🇵"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Dubai Luxury Experience",
            "destination": "Dubai, UAE",
            "source": "Any City",
            "duration": "5 Days / 4 Nights",
            "price": 2200,
            "category": "adventure",
            "budget": "luxury",
            "max_travelers": 4,
            "rating": 4.9,
            "icon": "🌆",
            "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Burj Khalifa", "Desert Safari", "Dubai Mall", "Palm Jumeirah"],
            "includes": ["5-Star Hotel", "All Meals", "Desert Safari", "Yacht Tour"],
            "image_emoji": "🇦🇪"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Swiss Alps Retreat",
            "destination": "Interlaken, Switzerland",
            "source": "Any City",
            "duration": "4 Days / 3 Nights",
            "price": 1800,
            "category": "mountains",
            "budget": "premium",
            "max_travelers": 6,
            "rating": 4.8,
            "icon": "⛰️",
            "image_url": "https://images.unsplash.com/photo-1508261305437-4f24efc34d50?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Jungfraujoch", "Paragliding", "Lake Thun", "Grindelwald"],
            "includes": ["Chalet Stay", "Breakfast & Dinner", "Ski Pass", "Train Pass"],
            "image_emoji": "🇨🇭"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Barcelona Beach & Culture",
            "destination": "Barcelona, Spain",
            "source": "Any City",
            "duration": "5 Days / 4 Nights",
            "price": 780,
            "category": "beach",
            "budget": "moderate",
            "max_travelers": 8,
            "rating": 4.6,
            "icon": "🏖️",
            "image_url": "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Sagrada Familia", "La Rambla", "Park Guell", "Barceloneta Beach"],
            "includes": ["Hotel", "Breakfast", "City Pass", "Tapas Tour"],
            "image_emoji": "🇪🇸"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Budget Bangkok Explorer",
            "destination": "Bangkok, Thailand",
            "source": "Any City",
            "duration": "5 Days / 4 Nights",
            "price": 450,
            "category": "food",
            "budget": "budget",
            "max_travelers": 10,
            "rating": 4.5,
            "icon": "🛕",
            "image_url": "https://images.unsplash.com/photo-1563492065599-3520f775eeed?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Grand Palace", "Floating Markets", "Street Food Tour", "Wat Pho"],
            "includes": ["Hostel", "Breakfast", "Tuk-Tuk Tour", "Street Food Walk"],
            "image_emoji": "🇹🇭"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Maldives Paradise",
            "destination": "Maldives",
            "source": "Any City",
            "duration": "6 Days / 5 Nights",
            "price": 3200,
            "category": "beach",
            "budget": "luxury",
            "max_travelers": 2,
            "rating": 5.0,
            "icon": "🏝️",
            "image_url": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Overwater Villa", "Snorkeling", "Sunset Cruise", "Underwater Restaurant"],
            "includes": ["Overwater Bungalow", "All-inclusive", "Water Sports", "Spa"],
            "image_emoji": "🇲🇻"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "New York City Buzz",
            "destination": "New York, USA",
            "source": "Any City",
            "duration": "4 Days / 3 Nights",
            "price": 1100,
            "category": "culture",
            "budget": "moderate",
            "max_travelers": 6,
            "rating": 4.7,
            "icon": "🗽",
            "image_url": "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Statue of Liberty", "Central Park", "Times Square", "Broadway Show"],
            "includes": ["Hotel", "Breakfast", "CityPASS", "Airport Shuttle"],
            "image_emoji": "🇺🇸"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Himalayan Trek",
            "destination": "Nepal",
            "source": "Any City",
            "duration": "8 Days / 7 Nights",
            "price": 600,
            "category": "mountains",
            "budget": "budget",
            "max_travelers": 12,
            "rating": 4.6,
            "icon": "🏔️",
            "image_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Annapurna Base Camp", "Pokhara", "Kathmandu Valley", "Sunrise at Poon Hill"],
            "includes": ["Lodge Stay", "All Meals on Trek", "Guide & Porter", "Permits"],
            "image_emoji": "🇳🇵"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Royal Rajasthan Road Trip",
            "destination": "Jaipur to Jaisalmer, India",
            "source": "Delhi",
            "duration": "6 Days / 5 Nights",
            "price": 42000,
            "category": "adventure",
            "budget": "moderate",
            "max_travelers": 5,
            "rating": 4.7,
            "icon": "🚗",
            "image_url": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Jaipur Forts", "Pushkar", "Jodhpur Blue City", "Jaisalmer Dunes"],
            "includes": ["SUV Rental", "Hotel Stay", "Driver", "Fuel"],
            "image_emoji": "🇮🇳"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "India Rail Explorer",
            "destination": "Delhi, Agra, Varanasi, Kolkata",
            "source": "Delhi",
            "duration": "7 Days / 6 Nights",
            "price": 36000,
            "category": "culture",
            "budget": "budget",
            "max_travelers": 6,
            "rating": 4.6,
            "icon": "🚆",
            "image_url": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=1200&q=80",
            "highlights": ["Taj Mahal", "Ganga Aarti", "Howrah Bridge", "Local Cuisine"],
            "includes": ["Train Tickets", "Hotel", "Breakfast", "Guided Tours"],
            "image_emoji": "🇮🇳"
        }
    ]


def _to_decimal(value: Any) -> Any:
    if isinstance(value, list):
        return [_to_decimal(item) for item in value]
    if isinstance(value, dict):
        return {key: _to_decimal(val) for key, val in value.items()}
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, int):
        return Decimal(value)
    return value


def seed_plans_to_dynamodb(
    table_name: str = "plans",
    region_name: str = "ap-south-1",
    endpoint_url: str | None = None,
    force: bool = False,
) -> Dict[str, Any]:
    """
    Seed TravelGo plans into DynamoDB.

    Requirements:
    - DynamoDB table exists
    - Primary key includes `plan_id` (String)

    Args:
        table_name: DynamoDB table name for plans.
        region_name: AWS region where table exists.
        endpoint_url: Optional DynamoDB endpoint URL (for local DynamoDB/testing).
        force: If False, seeding is skipped when table already has data.

    Returns:
        Summary dict with inserted/skipped counts.
    """
    try:
        boto3 = importlib.import_module("boto3")
    except ModuleNotFoundError:
        return {
            "status": "error",
            "error": "boto3 is not installed. Run: pip install boto3",
            "table": table_name,
        }

    endpoint = endpoint_url or os.getenv("DYNAMODB_ENDPOINT_URL")
    region = os.getenv("AWS_REGION", region_name)

    has_static_credentials = bool(os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"))
    has_profile = bool(os.getenv("AWS_PROFILE"))
    if not endpoint and not has_static_credentials and not has_profile:
        return {
            "status": "skipped",
            "reason": "dynamodb not configured (set DYNAMODB_ENDPOINT_URL or AWS credentials)",
            "inserted": 0,
            "skipped": 0,
            "table": table_name,
        }

    resource_kwargs: Dict[str, Any] = {"service_name": "dynamodb", "region_name": region}
    if endpoint:
        resource_kwargs["endpoint_url"] = endpoint
    if os.getenv("AWS_ACCESS_KEY_ID"):
        resource_kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID")
    if os.getenv("AWS_SECRET_ACCESS_KEY"):
        resource_kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY")
    if os.getenv("AWS_SESSION_TOKEN"):
        resource_kwargs["aws_session_token"] = os.getenv("AWS_SESSION_TOKEN")

    dynamodb = boto3.resource(**resource_kwargs)
    table = dynamodb.Table(table_name)

    try:
        if not force:
            existing_count = table.scan(Select="COUNT", Limit=1).get("Count", 0)
            if existing_count > 0:
                return {
                    "status": "skipped",
                    "reason": "table already has data",
                    "inserted": 0,
                    "skipped": 0,
                    "table": table_name,
                }

        plans = get_seed_plans_data()
        inserted = 0
        skipped = 0

        # Store same plan names once (idempotent by plan name).
        existing_names = set()
        scan_kwargs = {
            "ProjectionExpression": "#n",
            "ExpressionAttributeNames": {"#n": "name"},
        }
        while True:
            result = table.scan(**scan_kwargs)
            for item in result.get("Items", []):
                name = item.get("name")
                if name:
                    existing_names.add(name)
            if "LastEvaluatedKey" not in result:
                break
            scan_kwargs["ExclusiveStartKey"] = result["LastEvaluatedKey"]

        for plan in plans:
            if plan["name"] in existing_names:
                skipped += 1
                continue

            table.put_item(Item=_to_decimal(plan))
            inserted += 1

        return {
            "status": "success",
            "inserted": inserted,
            "skipped": skipped,
            "table": table_name,
        }

    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "table": table_name,
        }


if __name__ == "__main__":
    summary = seed_plans_to_dynamodb(table_name="plans", region_name="ap-south-1", force=False)
    print(summary)
