import plotly.express as px
import pandas as pd

def quantityAnalisys(data):
    if not data:
        return None
    
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="name",
        y="quantity",
        title="Quantity of your products",
        labels={'name': 'Product', "quantity": "quantityAnalisys"},
    )

    return fig.to_html(full_html=False)