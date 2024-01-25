from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

import json
import plotly
from vigilant_dev.visualization import create_plot

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_plot():
    try:
        fig = create_plot()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return f"""
        <html>
            <head>
                <title>3D Course Visualization</title>
                <style>
                    html, body {{
                        margin: 0;
                        padding: 0;
                        height: 100%;
                    }}
                    #divPlotly {{
                        height: 100vh;  /* 100% of the viewport height */
                        width: 100vw;   /* 100% of the viewport width */
                    }}
                </style>
            </head>
            <body>
                <div id='divPlotly'></div>
                <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
                <script type='text/javascript'>
                    var graphs = {graphJSON};
                    Plotly.newPlot('divPlotly', graphs, {{
                        responsive: true
                    }});
                </script>
            </body>
        </html>
        """
    except HTTPException as e:
        return f"<html><body><h2>Error: {e.detail}</h2></body></html>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
