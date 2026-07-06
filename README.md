# 🗺️ Apple Maps API: Local Search, Place Details, and Guides in Clean JSON

> The efficient, reliable, and developer-friendly way to use the Apple Maps API.

**Actor page:** [apify.com/johnvc/apple-maps-api](https://apify.com/johnvc/apple-maps-api?fpr=9n7kx3)
**Input schema:** [apify.com/johnvc/apple-maps-api/input-schema](https://apify.com/johnvc/apple-maps-api/input-schema?fpr=9n7kx3)

The Apple Maps API turns an Apple Maps lookup into clean, structured JSON. Pick a search mode, supply a query, and anchor it with a place name or coordinates. You get back local business listings (title, rating, reviews, address, GPS, place ID), curated Apple Maps guides, full place-detail objects, or the available refinement filters, depending on the mode. Built for local search, place enrichment, lead lists, and AI agent workflows.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-Apple-Maps-API.git
   cd Apify-Apple-Maps-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   uv run python apple-maps-api-example.py
   ```

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python apple-maps-api-example.py
```

## Why Use This Apple Maps API?

**Four modes, one Actor.** `search` returns the broad mix (local listings, guides, and refinements), `place` resolves a single rich place, `guide` returns curated collections, and `refinement` lists every filter available for a query.

**Geo-anchored.** Target by place name (`location`) or exact coordinates (`center`), and widen or narrow the viewport with `span`.

**Rich local listings.** Each result carries title, rating, review count, address, GPS coordinates, and a stable `place_id` you can reuse in `place` mode.

**Curated guides.** Apple Maps guides aggregate places under a theme (for example "Best coffee shops in Austin") with their publisher and item count.

**Discoverable filters.** `refinement` mode tells you the exact toggles, multi-select groups, and sort options available, so you can plan precise follow-up queries.

**Predictable, pay-per-use pricing.** A small per-run fee plus a per-item fee for the listings, guides, and details you keep. `max_results` keeps cost under control.

## Features

### Core Capabilities
- Four search modes: `search`, `place`, `guide`, `refinement`
- Place-name or coordinate anchoring, with an adjustable viewport `span`
- Sorting by default, distance, or rating
- Toggle and multi-select filters discovered via `refinement` mode
- Locale control for language and region

### Data Quality
- Local listings with title, rating, reviews, address, GPS, and `place_id`
- Curated guides with publisher and item count
- Result counts echoed on every response
- Consistent JSON shape across modes

## Usage Examples

### Local search
```json
{
  "search_mode": "search",
  "query": "coffee",
  "location": "Austin, Texas, United States",
  "max_results": 10
}
```

### Place detail by coordinates
```json
{
  "search_mode": "place",
  "query": "Apple Park Visitor Center",
  "center": "37.3346,-122.0090"
}
```

### Discover the filters for a query
```json
{
  "search_mode": "refinement",
  "query": "restaurants",
  "location": "Brooklyn, New York"
}
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `search_mode` | `str` | Yes | `search` | `search`, `place`, `guide`, or `refinement`. |
| `query` | `str` | Yes | - | Apple Maps search term, e.g. `coffee`, `plumbers in Brooklyn`. |
| `location` | `str` | one of | - | City-level place name. Either this or `center` is required. |
| `center` | `str` | one of | - | Center as `latitude,longitude`. Either this or `location` is required. |
| `span` | `str` | no | `0.5,0.5` | Viewport as `latDelta,lngDelta`; larger widens the radius. |
| `sort` | `str` | no | `default` | `default`, `distance`, or `ratings`. |
| `toggles` | `array` | no | - | Single-value filter keys (discover via `refinement` mode). |
| `multi_select_options` | `array` | no | - | Multi-value filter keys (chains, amenities, price tiers). |
| `open_at` | `int` | no | - | Unix timestamp for an "open at this time" filter (within 24h). |
| `locale` | `str` | no | `en-US` | Language and region code, e.g. `en-GB`, `fr-FR`. |
| `max_results` | `int` | no | `20` | Caps how many listings/guides are kept and billed; `0` = unlimited (safety-capped). |

## Output Format

A real `search` result for `coffee` in Austin (one row holding every result family; `local_results` and `guide_results` are trimmed to one item each).

```json
{
  "search_mode": "search",
  "search_parameters": { "query": "coffee", "location": "Austin, Texas, United States", "max_results": 5 },
  "result_counts": { "local": 5, "guide": 3, "place": 0, "refinement": 1 },
  "local_results": [
    {
      "position": 1,
      "place_id": "IA3069BB6296603C1",
      "title": "Fleet Coffee",
      "gps_coordinates": { "latitude": 30.2703261, "longitude": -97.7424645 },
      "rating": 75,
      "max_rating": 100,
      "reviews": 4,
      "address": "804 Congress Ave, Austin, TX 78701, United States",
      "link": "https://maps.apple.com/place?place-id=IA3069BB6296603C1&_provider=9902"
    }
  ],
  "guide_results": [
    {
      "position": 1,
      "title": "The Best Coffee Shops In Austin",
      "item_count": 15,
      "publisher": { "name": "The Infatuation" }
    }
  ],
  "refinement": { "toggles": [ "..." ], "multi_select": [ "..." ], "sort": [ "..." ] }
}
```

Apple Maps ratings use a 0-100 scale (`rating` out of `max_rating`) and include a breakdown by category. In `place` mode, `place_results` is populated with a richer object (photo gallery, about text, amenities, full weekly hours, and guide membership) instead.

---

## Use as an MCP tool

You can load the Apple Maps API as an MCP tool so assistants call it for you. The MCP server URL preloads just this one Actor:

```
https://mcp.apify.com/?tools=actors,docs,johnvc/apple-maps-api
```

Authenticate with OAuth in the browser when offered, or with your Apify API token (the same `APIFY_API_TOKEN` used by the Python example). Get a token at https://console.apify.com/settings/integrations and a free Apify account at https://apify.com?fpr=9n7kx3 .

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Apple Maps API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/apple-maps-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Apple Maps API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/apple-maps-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/apple-maps-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Apple Maps API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/apple-maps-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/apple-maps-api`, using OAuth when prompted.
5. Ask Claude to run the Apple Maps API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/apple-maps-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/apple-maps-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Apple Maps API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/apple-maps-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the Apple Maps API to power local search, place enrichment, and market research with reliable, structured results.*

Last Updated: 2026.07.06
