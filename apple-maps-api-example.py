"""
Example: call the Apple Maps API Apify Actor from Python.

The Actor has four search modes:
  search      local business listings + curated guides + the refinement object
  place       one rich place-detail object for a specific query
  guide       only curated Apple Maps guide collections
  refinement  the toggles, multi-select filters, and sort options for a query

This example runs 'search' for coffee in Austin and prints the local listings,
the curated guides, and the available refinements. Inputs are kept small so the
first run stays inexpensive (each listing and guide returned is billed).

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
Set it in a .env file (see .env.example) or export APIFY_API_TOKEN.
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not APIFY_API_TOKEN:
    raise SystemExit(
        "APIFY_API_TOKEN is not set. Copy .env.example to .env and add your key, "
        "or run: export APIFY_API_TOKEN=your_api_key_here"
    )

client = ApifyClient(APIFY_API_TOKEN)

# Anchor the search with 'location' (a place name) or 'center' (lat,lng).
# max_results caps how many listings/guides are kept and billed.
run_input = {
    "search_mode": "search",
    "query": "coffee",
    "location": "Austin, Texas, United States",
    "max_results": 5,
}

print(f"Apple Maps {run_input['search_mode']}: {run_input['query']} in {run_input['location']}")
run = client.actor("johnvc/apple-maps-api").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not start. Check your API token and inputs.")

for item in client.dataset(run.default_dataset_id).iterate_items():
    counts = item.get("result_counts", {})
    print(
        f"\nResult counts: {counts.get('local', 0)} local, "
        f"{counts.get('guide', 0)} guides, {counts.get('refinement', 0)} refinement\n"
    )

    print("Local listings:")
    for biz in item.get("local_results", []):
        rating = biz.get("rating")
        max_rating = biz.get("max_rating")
        rating_str = f"{rating}/{max_rating}" if rating is not None else "no rating"
        print(f"  {biz.get('position')}. {biz.get('title')}  ({rating_str}, {biz.get('reviews')} reviews)")
        print(f"     {biz.get('address')}")
        print(f"     place_id={biz.get('place_id')}")

    guides = item.get("guide_results", [])
    if guides:
        print("\nCurated guides:")
        for g in guides:
            publisher = (g.get("publisher") or {}).get("name", "")
            print(f"  - {g.get('title')} ({g.get('item_count')} places) by {publisher}")

    refinement = item.get("refinement", {})
    if refinement:
        toggles = refinement.get("toggles") or []
        multi = refinement.get("multi_select") or []
        sort = refinement.get("sort") or []
        print(
            f"\nAvailable refinements: {len(toggles)} toggles, "
            f"{len(multi)} multi-select groups, {len(sort)} sort options "
            f"(run search_mode='refinement' to see them all)."
        )
