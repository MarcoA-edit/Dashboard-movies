import streamlit as st
import pandas as pd
import plotly_express as px
import re
from PIL import Image
import subprocess
import requests
import plotly.graph_objects as go
from io import BytesIO
import os

image = Image.open("Nolan.jpg")
resized_image = image.resize((300, 150)) 

st.set_page_config(page_title="Nolan Movies", layout="wide", page_icon="🍿")
st.markdown("##")

colors = px.colors.sequential.Reds[::-4] 
df = pd.read_csv('df_final.csv')

t1, t2 = st.tabs(['Director','Movies'])

with t1:
    ##### Fazendo calculos nos DFs

    df_awards = df[['Title', 'Awards']]

    def extract_awards(awards_text):
        oscars_won = re.search(r'Won (\d+) Oscars?', awards_text)
        total_wins = re.search(r'(\d+) wins', awards_text)
        total_nominations = re.search(r'(\d+) nominations', awards_text)
        
        return {
            'Oscars_Won': int(oscars_won.group(1)) if oscars_won else 0,
            'Total_Wins': int(total_wins.group(1)) if total_wins else 0,
            'Total_Nominations': int(total_nominations.group(1)) if total_nominations else 0
        }

    awards_extracted = df_awards['Awards'].apply(extract_awards)
    awards_df = pd.DataFrame(awards_extracted.tolist())

    df_awards_separados = pd.concat([df_awards, awards_df], axis=1)

    total_indica = df_awards_separados['Total_Nominations'].sum()
    total_premiado = df_awards_separados['Total_Wins'].sum()
    total_oscar = df_awards_separados['Oscars_Won'].sum()

    premios_indicados = df_awards_separados[['Title', 'Total_Nominations']].sort_values(by='Total_Nominations', ascending=False)
    premios_ganhos = df_awards_separados[['Title', 'Total_Wins']].sort_values(by='Total_Wins', ascending=False)
    oscars_ganhos = df_awards_separados[['Title', 'Oscars_Won']].sort_values(by='Oscars_Won', ascending=False)

    df_rotten = df[['Title', 'Ratings_Value']].sort_values(by='Ratings_Value')
    df_imdb = df[['Title', 'imdbRating', 'imdbVotes']].sort_values(by='imdbRating')
    df_meta = df[['Title', 'Metascore']].sort_values(by='Metascore')

    df_bilheteria = df[['Title', 'BoxOffice']]
    df_bilheteria['BoxOffice'] = df_bilheteria['BoxOffice'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df_bilheteria = df_bilheteria.sort_values(by='BoxOffice', ascending=False)

    df_popular = df[['Title', 'imdbVotes']]
    df_popular['imdbVotes'] = df_bilheteria['BoxOffice'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df_popular = df_popular.sort_values(by='imdbVotes', ascending=False)

    df_direcao = df[['Title', 'Director']]
    nolan_diretor = df_direcao[df_direcao['Director'].str.contains('Christopher Nolan')]
    total_direcao = nolan_diretor.shape[0] 

    df_roteiro = df[['Title', 'Writer']]
    nolan_roterista = df_roteiro[df_roteiro['Writer'].str.contains('Christopher Nolan')]
    total_roteiro = nolan_roterista.shape[0] 

    ##### Montando Layout da página

    p1, p2 = st.columns([1,6])
    p1_cont = p1.container(height=450)
    p2_cont = p2.container(height=450)

    p3, p4, p5, p6, p7 = st.columns(5)
    p3_cont = p3.container(height=200)
    p4_cont = p4.container(height=200)
    p5_cont = p5.container(height=200)
    p6_cont = p6.container(height=200)
    p7_cont = p7.container(height=200)

    ##### Criando Gráficos

    fig_rotten = px.bar(df_rotten, x='Title', y='Ratings_Value',
                        labels={'Title' : ' ', 'Ratings_Value' : 'Porcentagem'}, height=350,
                        color_discrete_sequence=colors)
    fig_rotten.update_traces(texttemplate='%{y}%',
                            textposition='outside',
                            cliponaxis=False,
                            textfont=dict(size=20)) 
    fig_rotten.update_yaxes(visible=False)


    fig_imdb = px.bar(df_imdb, x='Title', y='imdbRating',
                        labels={'Title' : ' ', 'imdbRating' : 'Nota'},
                        color_discrete_sequence=colors,  height=350)
    fig_imdb.update_traces(texttemplate='%{y}',
                            textposition='outside',
                            cliponaxis=False,
                            textfont=dict(size=20)) 
    fig_imdb.update_yaxes(visible=False)


    fig_meta = px.bar(df_meta, x='Title', y='Metascore',
                        labels={'Title' : ' ', 'imdbRating' : 'Nota'},
                        color_discrete_sequence=colors,  height=350)
    fig_meta.update_traces(texttemplate='%{y}',
                            textposition='outside',
                            cliponaxis=False,
                            textfont=dict(size=20)) 
    fig_meta.update_yaxes(visible=False)

    ##### Escrevendo os indicadores

    pop = p2_cont.popover("Reviews 📈")
    site_avalia = pop.radio("Selecione o site de avaliação", ["Rotten Tomatoes 🍅", "IMDB :movie_camera:", "Metacritic Ⓜ️"])
    if site_avalia == 'Rotten Tomatoes 🍅':
        p2_cont.write("Rotten Tomatoes 🍅")
        p2_cont.plotly_chart(fig_rotten, use_container_width=True)
    if site_avalia == 'IMDB :movie_camera:':
        p2_cont.write("IMDB :movie_camera:")
        p2_cont.plotly_chart(fig_imdb, use_container_width=True)
    if site_avalia == "Metacritic Ⓜ️":
        p2_cont.write('Metacritic Ⓜ️')
        p2_cont.plotly_chart(fig_meta, use_container_width=True)


    p1_cont.image(resized_image, caption="Christopher Nolan")
    p1_cont.write(f"""📝 - ***Writer:*** {total_roteiro}""")
    p1_cont.write(f"""🎬 - ***Director:*** {total_direcao}""")
    p1_cont.write(f"""🎟️ - ***Nominated awards:*** {total_indica}""")
    p1_cont.write(f"""🏆 - ***Awards won:*** {total_premiado}""")
    p1_cont.write(f"""🏅 - ***Oscars won:*** {total_oscar}""")

    p3_cont.write("💸 - ***Biggest Box offices:***")
    for index, row in df_bilheteria.head(3).iterrows():
        p3_cont.write(f"**{row['Title']}** - ${row['BoxOffice']:,.2f}")

    p4_cont.write('🎟️ - ***Most awards nominee:***')
    for index, row in premios_indicados.head(3).iterrows():
        p4_cont.write(f"**{row['Title']}** - {row['Total_Nominations']}")

    p5_cont.write('🏆 - ***Most awards Won:***')
    for index, row in premios_ganhos.head(3).iterrows():
        p5_cont.write(f"**{row['Title']}** - {row['Total_Wins']}")

    p6_cont.write('🏅 - ***Most oscars Won:***')
    for index, row in oscars_ganhos.head(3).iterrows():
        p6_cont.write(f"**{row['Title']}** - {row['Oscars_Won']}")

    p7_cont.write(':movie_camera: - ***Most popular movies on IMDB:***')
    for index, row in df_popular.head(3).iterrows():
        p7_cont.write(f"**{row['Title']}** - {row['imdbVotes']}") 

with t2:
    df_coment = pd.read_csv('comentarios.csv')
    f1, f2 = st.columns(2)
    m1, m2, m3 = st.columns([1,1,3])

    m2_cont = m2.container(height=545)

    with m3:
        m3_cima, m4_cima, m5_cima = st.columns(3)
        m3_baixo, m4_baixo = st.columns([1,2])

        m3_cont_cima = m3_cima.container(height=265)
        m3_cont_baixo = m3_baixo.container(height=265)
        m4_cont_cima = m4_cima.container(height=265)
        m4_cont_baixo = m4_baixo.container(height=265)
        m5_cont_cima = m5_cima.container(height=265)
        

    
    with f1:
         pop3 = st.popover('Select movie')
         filme_selected = pop3.selectbox("Movies", df['Title'].unique())
         df_filtered = df[df['Title'] == filme_selected]

    if not df_filtered.empty:
        poster_url = df_filtered["Poster"].iloc[0]
        if poster_url and isinstance(poster_url, str):
            try:
                response = requests.get(poster_url)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))

                resized_img = img.resize((400, 600))

                m1.image(resized_img, use_container_width=False)
            except Exception as e:
                m1.write(f"Erro ao carregar ou redimensionar a imagem: {e}")
        else:
            m1.write("Pôster não disponível.")
    else:
        m1.write("Nenhum dado encontrado para o filme selecionado.")
    
    if not df_filtered.empty:
        imdb_rating = df_filtered["imdbRating"].iloc[0]
        if isinstance(imdb_rating, (int, float, str)) and imdb_rating != "N/A":
            try:
                imdb_rating = float(imdb_rating)

                if imdb_rating < 5:
                    gauge_color = "red"
                elif 5 <= imdb_rating < 7.5:
                    gauge_color = "yellow"
                else:
                    gauge_color = "green"

                fig_velo_imdb = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=imdb_rating,
                    title={'text': "IMDb"},
                    gauge={
                        'axis': {'range': [0, 10]},
                        'bar': {'color': gauge_color},
                        'steps': [
                            {'range': [0, 5], 'color': "rgba(255, 0, 0, 0.2)"},
                            {'range': [5, 7.5], 'color': "rgba(255, 255, 0, 0.2)"},
                            {'range': [7.5, 10], 'color': "rgba(0, 255, 0, 0.2)"},
                        ]
                    }
                ))

                fig_velo_imdb.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=240 
                )

                m3_cont_cima.plotly_chart(fig_velo_imdb, use_container_width=True)
            except Exception as e:
                m3_cont_cima.write(f"Erro ao processar o IMDb Rating: {e}")
        else:
            m3_cont_cima.write("IMDb Rating não disponível.")
    else:
        m2_cont_cima.write("Nenhum dado encontrado para o filme selecionado.")
    
    if not df_filtered.empty:
        metascore = df_filtered["Metascore"].iloc[0]
        
        # Tenta converter o Metascore para float
        try:
            metascore = float(metascore)
            
            if metascore < 50:
                gauge_color = "red"
            elif 50 <= metascore < 75:
                gauge_color = "yellow"
            else:
                gauge_color = "green"

            fig_velo_meta = go.Figure(go.Indicator(
                mode="gauge+number",
                value=metascore,
                title={'text': "Metascore"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': gauge_color},
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(255, 0, 0, 0.2)"},
                        {'range': [50, 75], 'color': "rgba(255, 255, 0, 0.2)"},
                        {'range': [75, 100], 'color': "rgba(0, 255, 0, 0.2)"},
                    ]
                }
            ))

            fig_velo_meta.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                height=240
            )

            m4_cont_cima.plotly_chart(fig_velo_meta, use_container_width=True)

        except Exception as e:
            m4_cont_cima.write("Erro ao exibir o Metascore.")
    else:
        m4_cont_cima.write("Nenhum dado encontrado para o filme selecionado.")

    if not df_filtered.empty:
        rotten_str = df_filtered["Ratings_Value"].iloc[0]
        try:
            # Remove o símbolo de porcentagem e converte para float
            rotten = float(rotten_str.strip('%'))

            # Define a cor do gauge com base no valor
            if rotten < 50:
                gauge_color = "red"
            elif 50 <= rotten < 75:
                gauge_color = "yellow"
            else:
                gauge_color = "green"

            # Criação do gráfico de gauge
            fig_velo_rotten = go.Figure(go.Indicator(
                mode="gauge+number",
                value=rotten,
                title={'text': "Rotten"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': gauge_color},
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(255, 0, 0, 0.2)"},
                        {'range': [50, 75], 'color': "rgba(255, 255, 0, 0.2)"},
                        {'range': [75, 100], 'color': "rgba(0, 255, 0, 0.2)"},
                    ]
                }
            ))

            # Configurações de layout
            fig_velo_rotten.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                height=240
            )

            # Renderiza o gráfico no Streamlit
            m5_cont_cima.plotly_chart(fig_velo_rotten, use_container_width=True)

        except Exception as e:
            m5_cont_cima.write("Erro ao exibir o Metascore.")
    else:
        m5_cont_cima.write("Nenhum dado encontrado para o filme selecionado.")

    plot = df_filtered['Plot'].iloc[0]
    relesed = df_filtered['Released'].iloc[0]
    runtime= df_filtered['Runtime'].iloc[0]
    genre= df_filtered['Genre'].iloc[0]
    actors= df_filtered['Actors'].iloc[0]
    writer= df_filtered['Writer'].iloc[0]
    director= df_filtered['Director'].iloc[0]
    awards= df_filtered['Awards'].iloc[0]
    boxoffice= df_filtered['BoxOffice'].iloc[0]
        

    m2_cont.subheader('Information')
    m2_cont.markdown(f"**Plot:** {plot}")
    m2_cont.markdown(f"**Relesed:** {relesed}")
    m2_cont.markdown(f"**Runtime:** {runtime}")
    m2_cont.markdown(f"**Actors:** {actors}")
    m2_cont.markdown(f"**Writer:** {writer}")
    m2_cont.markdown(f"**Director:** {director}")
    m2_cont.markdown(f"**Awards:** {awards}")
    m2_cont.markdown(f"**Box Office:** {boxoffice}")

    m3_cont_baixo.subheader('Comments')
    
    comments = df_coment[df_coment['Title'].isin(df_filtered['Title'])]

    for index, row in comments.iterrows():
        m3_cont_baixo.write(f"**{row['User']}** - {row['Comment']}")
    
    with m3_cont_baixo:
        pop4 = st.popover('Add comment')
        movie_title = df_filtered["Title"].iloc[0]

        user_name = pop4.text_input("Name")
        user_comment = pop4.text_area("Coment")

        
        if pop4.button("Send"):
            if user_name.strip() and user_comment.strip():
                
                new_data = {
                    "Title": [movie_title],
                    "User": [user_name],
                    "Comment": [user_comment]
                }
                new_df = pd.DataFrame(new_data)
                
                file_path = "comentarios.csv"

                if os.path.exists(file_path):
                    existing_df = pd.read_csv(file_path)
                    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                else:
                    updated_df = new_df

                updated_df.to_csv(file_path, index=False)
                pop4.success("Success")
            else:
                pop4.error("Empty Box")


    with m4_cont_baixo:
        pop5 = st.popover('Compare')

        available_movies = df[~df['Title'].isin(df_filtered['Title'])]['Title'].unique()
        filme_compare = pop5.selectbox("Movies", available_movies, key='1')
        df_filtered2 = df[df['Title'] == filme_compare]

        type_of_compare = pop5.radio("Type of compare",["Imdb", "Rotten Tomatoes", "Metascore", "Box Office", "Imdb Votes"])
        if type_of_compare == "Imdb":
           df_concat = pd.concat([df_filtered[['Title', 'imdbRating']], df_filtered2[['Title', 'imdbRating']]], ignore_index=True)
           y_bar = df_concat['imdbRating']

        if type_of_compare == "Rotten Tomatoes":
           df_concat = pd.concat([df_filtered[['Title', 'Ratings_Value']], df_filtered2[['Title', 'Ratings_Value']]], ignore_index=True)
           y_bar = df_concat['Ratings_Value']

        if type_of_compare == "Metascore":
           df_concat = pd.concat([df_filtered[['Title', 'Metascore']], df_filtered2[['Title', 'Metascore']]], ignore_index=True)
           y_bar = df_concat['Metascore']
        
        if type_of_compare == "Box Office":
           df_concat = pd.concat([df_filtered[['Title', 'BoxOffice']], df_filtered2[['Title', 'BoxOffice']]], ignore_index=True)
           y_bar = df_concat['BoxOffice']
           
        if type_of_compare == "Imdb Votes":
           df_concat = pd.concat([df_filtered[['Title', 'imdbVotes']], df_filtered2[['Title', 'imdbVotes']]], ignore_index=True)
           y_bar = df_concat['imdbVotes']

        fig_compare = px.bar(df_concat, x='Title', y=y_bar,
                        labels={'Title' : ' ', 'Ratings_Value' : 'Porcentagem'}, height=200,orientation='v',
                        color_discrete_sequence=colors)
        fig_compare.update_traces(texttemplate='%{y}',
                            textposition='outside',
                            cliponaxis=False,
                            textfont=dict(size=20)) 
        fig_compare.update_yaxes(visible=False)
        st.plotly_chart(fig_compare)

#### Nessa parte é feita o request na API OMDB, por enquanto só fuciona com o código baixado

    #pop2 = st.popover("Adicionar filme")
    #with pop2:
    #    popl1 = st.columns(1)
    #    popb1, popb2 = st.columns(2)

    #user_input = popl1[0].text_area("Adicionar Filme:", height=70)

    #if popb1.button("Salvar"):
        #if user_input:
            #texto = pd.DataFrame({"Filme": [user_input]})
           #texto.to_csv('carga.csv', index=False)
           # try:
                #subprocess.run(['python', 'request.py'], check=True)
                
                #subprocess.run(['python', 'convert.py'], check=True)
                
                #subprocess.run(['python', 'final_convert.py'], check=True)
                
                #popb2.success("Carga efetuada com sucesso!")
            #except subprocess.CalledProcessError as e:
                #popb2.error(f"Erro ao executar um dos scripts: {e}")
            #except Exception as e:
                #popb2.error(f"Erro inesperado: {e}")
        #else:
            #popb2.warning("Por favor, escreva algo antes de salvar.")



