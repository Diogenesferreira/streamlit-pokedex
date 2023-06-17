import streamlit as st
import requests
from PIL import Image

# Configurar o estilo para remover o texto "Made with Streamlit"

im = Image.open("pokeball.ico")
st.set_page_config(
    page_title="Pokedex",
    page_icon=im
)

# Remover a barra de configuração
st.set_option('deprecation.showfileUploaderEncoding', False)

st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

def buscar_imagem_pokemon(pokemon_id):
    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{pokemon_id}.gif"
    response = requests.get(url)
    return response.content

def buscar_informacoes_pokemon(pokemon):
    """
    Busca as informações do Pokémon, incluindo número, nome, altura, peso, habilidades, status e tipos.
    :param pokemon: Nome ou número do Pokémon.
    :return: Dicionário contendo as informações do Pokémon.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    response = requests.get(url)
    data = response.json()

    if 'id' not in data or 'name' not in data or 'height' not in data or 'weight' not in data or 'abilities' not in data or 'stats' not in data or 'types' not in data:
        raise ValueError("As informações do Pokémon não estão completas.")

    num_pokemon = data['id']
    nome_pokemon = data['name']
    altura_pokemon = data['height']
    peso_pokemon = data['weight']
    habilidades_pokemon = [ability['ability']['name'] for ability in data['abilities']]
    status_pokemon = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    tipos_pokemon = [type_data['type']['name'] for type_data in data['types']]

    return {
        'num_pokemon': num_pokemon,
        'nome_pokemon': nome_pokemon,
        'altura_pokemon': altura_pokemon,
        'peso_pokemon': peso_pokemon,
        'habilidades_pokemon': habilidades_pokemon,
        'status_pokemon': status_pokemon,
        'tipos_pokemon': tipos_pokemon
    }

col_titulo1, col_titulo2, col_titulo3 = st.columns(3)

with col_titulo2:
   st.title("Pokedex")

st.write("---")  # Adiciona uma linha para separar os elementos

#Container com os campos de busca e etc
with st.container():

   col1, col2, col3 = st.columns([4,1,3])

   with col1:
       pokemon_input = st.text_input("Digite o nome ou número do Pokémon")

       coluna_buscar, coluna_voltar, coluna_avancar = st.columns(3)

       with coluna_buscar:
          buscar_button = st.button("Buscar")

       with coluna_voltar:
            voltar_button = st.button("<< Anterior")

       with coluna_avancar:
            avancar_button = st.button("Próximo >>")

   if buscar_button:
    if pokemon_input:
        pokemon_info = buscar_informacoes_pokemon(pokemon_input)
        id_pokemon = pokemon_info['num_pokemon']
        nome = pokemon_info['nome_pokemon']
        altura = pokemon_info['altura_pokemon']
        peso = pokemon_info['peso_pokemon']
        stats = pokemon_info['status_pokemon']
        tipos = pokemon_info['tipos_pokemon']
        imagem = buscar_imagem_pokemon(id_pokemon)

        with col3:
            st.image(imagem, caption=nome, width=160)

        st.write("---")  # Adiciona uma linha para separar os elementos
        st.write("Status Base do Pokemon")

        with st.container():
            col_ststus1, col_ststus2, col_ststus3, col_ststus4, col_ststus5, col_ststus6 = st.columns([1,1,1,1,1,1])
           
            with col_ststus1:
                st.info(f"**HP:** {stats['hp']}")

            with col_ststus2:
                st.info(f"**ATK:** {stats['attack']}")

            with col_ststus3:
                st.info(f"**DEF:** {stats['defense']}")

            with col_ststus4:
                st.info(f"**SPD:** {stats['speed']}")

            with col_ststus5:
                st.info(f"**S.ATK:** {stats['special-attack']}")

            with col_ststus6:
                st.info(f"**S.DEF** {stats['special-defense']}")
st.write("---")  # Adiciona uma linha para separar os elementos