from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
'''
    typing.Any: Represents any type of data. Used for type annotations.
    httpx: A library in Python that allows you to make HTTP requests (GET, POST, etc.). It is similar to the 'requests' library but supports asynchronous (async) operations.
    FastMCP: A server class that helps quickly initialize the MCP (Model Context Protocol) infrastructure.
'''

# Inıtialize FastMCP server
mcp = FastMCP("Weather")
'''
    Starts an MCP server named "Weather".
    Through this server, you can define tools (@mcp.tool()), resources (@mcp.resource()), and prompts (@mcp.prompt()).
'''

# API Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
'''
    NWS_API_BASE: The base URL of the National Weather Service (NWS).
    USER_AGENT: A header used to identify the client making the HTTP request (acts like a browser).
'''

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status
            return response.json()
        except Exception:
            return None
        
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]   # Extracts the "properties" sub-dictionary from the feature dictionary.
    return f"""
    Event: {props.get('event', 'Unknown')}
    Area: {props.get('areaDesc', 'Unknown')}
    Severity: {props.get('severity', 'Unknown')}
    Description: {props.get('description', 'No description available.')}
    Instructions: {props.get('instruction', 'No specific instruction provided.')}
    """

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f'{NWS_API_BASE}/alerts/active/area/{state}'
    data = await make_nws_request(url)
    
    if not data or 'features' not in data:
        return "Unable to fetch alerts or no alerts found."
    
    if not data['features']:
        return 'No active alerts for this state.'
    
    alerts = [format_alert(feature) for feature in data['features']]
    return '\n---\n'.join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f'{NWS_API_BASE}/points/{latitude},{longitude}'
    points_data = await make_nws_request(points_url)

    if not points_data:
        return 'Unable to fetch forecast data for this location.'
    
    # Get the forecast URL from the points response
    forecast_url = points_data['properties']['forecast']
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return 'Unable to fetch detailed forecast.'
    
    # Format the periods into a readable forecast
    periods = forecast_data['properties']['periods']
    forecasts = []
    ''' 
    This creates an empty list.
    Weather forecast text for each day will be added to this list shortly.
    '''
    for period in periods[:5]:
        '''
        [:5] → Takes the first 5 elements (from index 0 to 4).
        This way, the user is shown the weather forecast for 5 days / periods.
        '''
        forecast = f'''
        {period['name']}:
        Temperature: {period['temperature']}°{period['temperatureUnit']}
        Wind: {period['windSpeed']} {period['windDirection']}
        Forecast: {period['detailedForecast']}
        '''
        forecasts.append(forecast)

    return '\n---\n'.join(forecasts)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
    '''
    If not included: Claude or Cursor won't be able to see or run your code.
    '''