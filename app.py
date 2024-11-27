import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração inicial do layout do Streamlit
st.set_page_config(layout="wide", page_title="Dashboard Populacional")

# Título do Dashboard
st.title("📊 Projeções Populacionais do Brasil  (2000-2070)")
st.markdown("Explore as projeções populacionais do Brasil, em um período de 70 anos. Escolha filtros para visualizar os dados de forma interativa.")


# Leitura do arquivo XLSX
df = pd.read_excel("dados.xlsx")

# Filtragem para opções do painel
anos_disponiveis = sorted(df["ANO"].unique())
localidades_disponiveis = sorted(df["LOCAL"].unique())

# Filtros na barra lateral
st.sidebar.title("Filtros")
ano_selecionado = st.sidebar.selectbox("Selecione o ano:", anos_disponiveis)
localidade_selecionada = st.sidebar.selectbox("Selecione a localidade:", localidades_disponiveis)

# Filtrar os dados com base nos filtros selecionados
df_filtrado = df[(df["ANO"] == ano_selecionado) & (df["LOCAL"] == localidade_selecionada)]

# Layout de colunas
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

if not df_filtrado.empty:
    # Gráfico 1: População total por sexo (gráfico de pizza)
    df_total = pd.DataFrame({
        "Sexo": ["Homens", "Mulheres"],
        "População": [df_filtrado["POP_H"].values[0], df_filtrado["POP_M"].values[0]],
    })

    fig_pizza = px.pie(
        df_total,
        names="Sexo",
        values="População",
        title=f"População Total por Sexo ({localidade_selecionada} - {ano_selecionado})",
        color="Sexo",
        color_discrete_sequence=px.colors.sequential.RdBu,
        hole=0.3,  # Criação de gráfico de pizza com um "buraco" no meio (estilo doughnut)
        labels={"População": "População Total", "Sexo": "Sexo"}
    )
    fig_pizza.update_layout(
        title_font=dict(family="Arial", size=20, color="black"),
        legend_title="Sexo",
        legend=dict(x=0.85, y=0.95, traceorder="normal", font=dict(family="Arial", size=12), bgcolor="rgba(255, 255, 255, 0.5)"),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)"
    )
    col1.plotly_chart(fig_pizza, use_container_width=True)

    # Gráfico 2: Crianças e jovens (gráfico de radar/spider chart)
    categorias_criancas = ["0-1 anos", "0-4 anos", "0-14 anos"]
    valores_criancas = [
        df_filtrado["0-1_T"].values[0],
        df_filtrado["0-4_T"].values[0],
        df_filtrado["0-14_T"].values[0],
    ]

    fig_radar_criancas = go.Figure()
    fig_radar_criancas.add_trace(go.Scatterpolar(
        r=valores_criancas,
        theta=categorias_criancas,
        fill='toself',
        name='Crianças e Jovens',
        line=dict(color="crimson", width=2),
        marker=dict(size=8, color="crimson")
    ))
    fig_radar_criancas.update_layout(
        title=f"Crianças e Jovens ({localidade_selecionada} - {ano_selecionado})",
        polar=dict(radialaxis=dict(visible=True, tickangle=90)),
        showlegend=False,
        font=dict(family="Arial", size=14, color="black"),
        title_font=dict(family="Arial", size=20, color="black"),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)"
    )
    col2.plotly_chart(fig_radar_criancas, use_container_width=True)

    # Gráfico 3: Evolução populacional (gráfico de linha)
    df_evolucao = df[(df["LOCAL"] == localidade_selecionada)].groupby("ANO")[["POP_T"]].sum().reset_index()

    fig_linha = px.line(
        df_evolucao,
        x="ANO",
        y="POP_T",
        title=f"Evolução Populacional Total ({localidade_selecionada})",
        labels={"POP_T": "População Total", "ANO": "Ano"},
        line_shape="linear",  # Linha mais suave
        markers=True,  # Marcação dos pontos da linha
        color_discrete_sequence=["#EF553B"]
    )
    fig_linha.update_layout(
        title_font=dict(family="Arial", size=20, color="black"),
        xaxis=dict(showgrid=False, zeroline=False, tickangle=45),
        yaxis=dict(showgrid=True, zeroline=False),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(family="Arial", size=14, color="black"),
        hovermode="x unified"  # Exibição unificada de todos os valores no hover
    )
    col3.plotly_chart(fig_linha, use_container_width=True)

    # Gráfico 4: Adolescentes e adultos (gráfico de barras empilhadas)
    df_adultos = pd.DataFrame({
        "Faixa Etária": ["15-17 anos", "18-21 anos", "15-59 anos", "15-64 anos"],
        "População": [
            df_filtrado["15-17_T"].values[0],
            df_filtrado["18-21_T"].values[0],
            df_filtrado["15-59_T"].values[0],
            df_filtrado["15-64_T"].values[0],
        ],
    })

    fig_adultos = px.bar(
        df_adultos,
        x="Faixa Etária",
        y="População",
        title=f"Adolescentes e Adultos ({localidade_selecionada} - {ano_selecionado})",
        labels={"População": "População Total", "Faixa Etária": "Faixa Etária"},
        color="Faixa Etária",
        color_discrete_sequence=px.colors.sequential.Plasma,
        barmode="stack",  # Barras empilhadas
        height=400
    )
    fig_adultos.update_layout(
        title_font=dict(family="Arial", size=20, color="black"),
        xaxis=dict(showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(family="Arial", size=14, color="black")
    )
    col4.plotly_chart(fig_adultos, use_container_width=True)

    # Gráfico 5: Idosos (gráfico de radar/spider chart)
    categorias_idosos = ["60+ anos", "65+ anos", "80+ anos"]
    valores_idosos = [
        df_filtrado["60+_T"].values[0],
        df_filtrado["65+_T"].values[0],
        df_filtrado["80+_T"].values[0],
    ]

    fig_radar_idosos = go.Figure()
    fig_radar_idosos.add_trace(go.Scatterpolar(
        r=valores_idosos,
        theta=categorias_idosos,
        fill='toself',
        name='Idosos',
        line=dict(color="forestgreen", width=2),
        marker=dict(size=8, color="forestgreen")
    ))
    fig_radar_idosos.update_layout(
        title=f"Idosos ({localidade_selecionada} - {ano_selecionado})",
        polar=dict(radialaxis=dict(visible=True, tickangle=90)),
        showlegend=False,
        font=dict(family="Arial", size=14, color="black"),
        title_font=dict(family="Arial", size=20, color="black"),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)"
    )
    col5.plotly_chart(fig_radar_idosos, use_container_width=True)

    # Tabela de resumo
    st.write("### Resumo dos Dados Filtrados")
    st.dataframe(df_filtrado)

else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
