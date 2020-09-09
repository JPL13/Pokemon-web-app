
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from sklearn.decomposition import PCA


# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """


    # read in data    
    df =pd.read_csv('./data/Pokemon.csv')

    # First Plot compares Legendary vs normal Pokemons

    x = df[df["Legendary"] == True] # Legendary
    y = df[df["Legendary"] == False]  # Normal

    trace1 = go.Scatterpolar(
      r = [x['HP'].mean(),x['Attack'].mean(),x['Defense'].mean(),x['Sp. Atk'].mean(),x['Sp. Def'].mean(),x['Speed'].mean(),x["HP"].mean()],
      theta = ['HP','Attack','Defense','Sp. Atk','Sp. Def','Speed','HP'],
      fill = 'toself',
      name = 'Legendary'
    )

    trace0 = go.Scatterpolar(
      r = [y['HP'].mean(),y['Attack'].mean(),y['Defense'].mean(),y['Sp. Atk'].mean(),y['Sp. Def'].mean(),y['Speed'].mean(),y["HP"].mean()],
      theta = ['HP','Attack','Defense','Sp. Atk','Sp. Def','Speed','HP'],
      fill = 'toself',
      name = 'Normal'
    )

    data = [trace0, trace1]

    layout = go.Layout(
      polar = dict(
        radialaxis = dict(
          visible = True,
          range = [0, 200]
        )
      ),
      showlegend = True,
      title = "{} vs {} Mean Values Comparison".format('Legendary', 'Normal')
    )
    fig0 = go.Figure(data=data, layout=layout)

    # Second chart shows the Histogram of total score of Legendary vs Normal pokemon
    x = df[df["Legendary"] == True] # Subset Legendary Pokemon
    y = df[df["Legendary"] == False] # Subset Normal Pokemon

    trace1 = go.Histogram(
        x=x['Total'],
        opacity=0.75,
        name = 'Legendary',
        marker=dict(color='rgba(171, 50, 96, 0.6)'))
    trace2 = go.Histogram(
        x=y['Total'],
        opacity=0.75,
        name = "Normal",
        marker=dict(color='rgba(12, 50, 196, 0.6)'))

    data = [trace1, trace2]
    layout = go.Layout(barmode='overlay',
                       title=' Total Scores of Legendary vs Normal Pokemons',
                       xaxis=dict(title='Total Scores'),
                       yaxis=dict( title='Count'),
    )
    fig1 = go.Figure(data=data, layout=layout)


    ## Third plot is a Categorical bubble chart with Attack on X-axis, Defense on Y-axis and Speed as size for Top 50
    ## Legendary vs Top 50 Normal Pokemons
    # Prepare data 
    l_top=x.sort_values(by=['Total'], ascending=False).iloc[:50]
    n_top=y.sort_values(by=['Total'], ascending=False).iloc[:50]
    df20= pd.concat([l_top,n_top])

    # plot
    sizeref = max(df['Speed'])/(500)

    trace1 = go.Scatter(
        x=l_top["Attack"],
        y=l_top["Defense"],
        mode='markers',
        name="Legendary",
        text=l_top["Name"],
        marker=dict(
            symbol='circle',
            sizemode='area',
            size=l_top["Speed"],
            sizeref=sizeref,
            line=dict(
                width=2
            ),
        )
    )
    trace0 = go.Scatter(
        x=n_top["Attack"],
        y=n_top["Defense"],
        mode='markers',
        name='Normal',
        text=n_top["Name"],
        marker=dict(
            sizemode='area',
            size=n_top["Speed"],
            sizeref=sizeref,
            line=dict(
                width=2
            ),
        )
    )

    data = [trace0, trace1]
    layout = go.Layout(
        title='Attack vs Defense of Top 50 Legendary and Normal Pokemons(Bubble size represents Speed)',
        xaxis=dict(
            title='Attack',
            gridcolor='rgb(255, 255, 255)',
            range=[0,200]
        ),
        yaxis=dict(
            title='Defense',
            gridcolor='rgb(255, 255, 255)',
            range=[0,200]
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
    )

    fig2 = go.Figure(data=data, layout=layout)

    ### Fourth plot is a PCA scatter plot
    df_new = df.replace({True: 'Legendary', False: 'Normal'})
    features = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

    pca = PCA()
    components = pca.fit_transform(df[features])
    labels = {
        str(i): f"PC {i+1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }

    fig3 = px.scatter_matrix(
        components,
        labels=labels,
        dimensions=range(6),
        title='Pairwise Principal Components Scatter Plot ', 
        color=df_new["Legendary"]
    )
    fig3.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', width=800,
    height=800)

    fig3.update_traces(diagonal_visible=False )


    ### Fifth pot show an 2D PCA Scatter Plot
    pca = PCA(n_components=2)
    components = pca.fit_transform(df[features])
    total_var = pca.explained_variance_ratio_.sum() * 100

    fig4 = px.scatter(components, 
                     x=0,
                     y=1, 
                     color=df_new["Legendary"],
                     title=f'Total Explained Variance with 2 PC: {total_var:.2f}%',
                     labels={'0': 'PC 1', '1': 'PC 2'}



    )

    ### Sixth pot show an 3D PCA Scatter Plot

    pca = PCA(n_components=3)
    components = pca.fit_transform(df[features])

    total_var = pca.explained_variance_ratio_.sum() * 100

    fig5 = px.scatter_3d(
        components, x=0, y=1, z=2, color=df_new["Legendary"],
        title=f'Total Explained Variance with 3 PC: {total_var:.2f}%',
        labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}

    )
    

    # append all charts to the figures list
    figures = []
    figures.append(fig0)
    figures.append(fig1)
    figures.append(fig2)
    figures.append(fig3)
    figures.append(fig4)
    figures.append(fig5)

    return figures