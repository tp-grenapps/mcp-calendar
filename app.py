from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

from gcalendar import GoogleCalendarAPI

mcp = FastMCP(name="calendar", host="127.0.0.1", port="8123")

@mcp.tool()
def list_items(arg):
    """List the events or tasks in google calendar account
    
    Args: none
    """
    try:
        cal = GoogleCalendarAPI()    
        return cal.list_items()
    except Exception as e:
        print("Error encountered in app.list_items: " + str(e))
        return str(e)

@mcp.tool()
def add_event(arg):
    """Send an event to Google Calendar
    
    Args: an object with the following properties: summary<string>, location<string>, description<string>, startTime<datetime>, endTime<datetime>
    """
    try:
        email = GoogleCalendarAPI() 
        eventx = {
            'summary':arg['summary'],
            'location':arg['location'],
            'description':arg['description'],
            'startTime':  arg["startTime"],
            'endTime':  arg["endTime"],
        }   
        email.add_event(event=eventx)
        
        return "" 
    except Exception as e:
        print("Error encountered in app.send_message: " + str(e))
        return str(e)

if __name__ == "__main__":
    # Initialize and run the server
    # mcp.run(transport='stdio')
    transport = "stdio"
    # transport = "sse"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")