import streamlit as st
from pathlib import Path
from PIL import Image, ImageOps

st.title("Bio Page")

# ---------- TODO: Replace with your own info ----------
NAME = "Phil and Ricardo"
PROGRAM = "Video Game Reception"
INTRO = (
    "Hi, welcome to our streamlit page. This project is about the cost of development of well received video games from 2015-2025(1/year). It includes the ratings of the video games and the copies they have sold/year since their release. We have also included a geopleth to show where in the world have they been sold and will have a bigger list of video games starting from 1990's to the current year. Of course we ran into some problems of trying to find out the information to create the databases, so there is most likely going to be skewed data. The only part that is the most accurate would be their individual ratings. The databases that were created are the csv files (top10), (10salehistory), and (rating). Only the csv file (vgsales) was taken from kaggle. What is the difference between the (10salehistory) and (vgsales) file? Well the major difference between the two is that (10salehistory) is the total amount of copies sold since their release date. It is only about the well received video games from 2015-2025(1/year). On the other hand, (vgsales) is where in the world video games from 1990-2025 have been sold."
)

FUN_FACTS = [
    "As of September 2024, the most expensive video game to be developed is Genshin Impact. It is due to its live-service element that costs ~$200m/year.",
    "Indie games are more likely to earn bigger profits as the development costs are less.",
    "Concord, released in August 2024, shut down after two weeks of its release with a full refund to all customers who bought the game."
]

SOURCES_URL = [
    "https://www.gamesradar.com/games/open-world/its-taken-4-years-and-roughly-dollar900-million-but-genshin-impact-is-a-better-open-world-rpg-than-ever-after-update-50/",
    "https://gamemaker.io/en/blog/cost-of-making-a-game",
    "https://gamerant.com/biggest-games-flopped-commercially/"
]

def find_photo(filename="photo(?).jpg"):
    # Photo was saved in assets folder
    try:
        script_dir = Path(__file__).resolve().parent
    except NameError:
        script_dir = Path.cwd()
 
    candidates = [
        script_dir / "assets" / "photo(?).jpg",          # pages/assets/...
        script_dir.parent / "assets" / "photo(?).jpg",   # root/assets/... (common)
        Path("assets") / "photo(?).jpg",                 # cwd/assets/...
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None
 
photo_src = find_photo("photo(?).jpg")  # Put a file in repo root or set a URL

# ---------- Layout ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center") 

with col1: 
    if photo_src:
        img = Image.open(photo_src)
        img = ImageOps.exif_transpose(img)
        st.image(img, caption=NAME, use_container_width=True)
    else:
        st.info( "📷 Place Ren_Photo.jpg inside an assets/ folder at the app root " 
                "or update the path in find_photo()." )
        
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.markdown("### Fun facts")
for i, f in enumerate(FUN_FACTS, start=1):
    st.write(f"- {f}")

st.markdown("### Sources")
for i, f in enumerate(SOURCES_URL, start=1):
    st.write(f"- [{f}]({f})")
    
st.divider()
st.caption("Edit pages/1_Bio.py to customize this page.")
