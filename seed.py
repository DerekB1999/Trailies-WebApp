from sqlmodel import Session, SQLModel, select

from database import engine
from models import Trail
from schemas import Difficulty


def seed():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        if session.exec(select(Trail)).first():
            print("Database already seeded, skipping.")
            return

        trails = [
            Trail(
                name="Mount Holyoke Range Loop",
                distance=6.5,
                lat=42.3009,
                lon=-72.5167,
                alt=935.0,
                surface="rock",
                difficulty=Difficulty.hard,
                bike_friendly=False,
                dog_friendly=True,
                description="Challenging ridge hike with panoramic views of the Pioneer Valley.",
            ),
            Trail(
                name="Norwottuck Rail Trail",
                distance=10.8,
                lat=42.3251,
                lon=-72.5199,
                alt=120.0,
                surface="paved",
                difficulty=Difficulty.easy,
                bike_friendly=True,
                dog_friendly=True,
                description="Popular flat rail trail connecting Amherst to Northampton, great for biking.",
            ),
            Trail(
                name="Amethyst Brook Conservation Area",
                distance=2.4,
                lat=42.4095,
                lon=-72.5272,
                alt=300.0,
                surface="dirt",
                difficulty=Difficulty.easy,
                bike_friendly=False,
                dog_friendly=True,
                description="Short wooded hike with a scenic brook and small waterfalls.",
            ),
            Trail(
                name="Mount Sugarloaf Loop",
                distance=3.2,
                lat=42.4906,
                lon=-72.5787,
                alt=652.0,
                surface="rock",
                difficulty=Difficulty.medium,
                bike_friendly=False,
                dog_friendly=True,
                description="Steady climb to a summit with excellent views of the Connecticut River.",
            ),
            Trail(
                name="Fort River Birding and Nature Trail",
                distance=1.8,
                lat=42.3432,
                lon=-72.4876,
                alt=90.0,
                surface="gravel",
                difficulty=Difficulty.easy,
                bike_friendly=True,
                dog_friendly=False,
                description="Flat trail through wetlands, ideal for birdwatching and peaceful walks.",
            ),
            Trail(
                name="Lawrence Swamp Trail",
                distance=2.0,
                lat=42.3663,
                lon=-72.5057,
                alt=110.0,
                surface="boardwalk",
                difficulty=Difficulty.easy,
                bike_friendly=False,
                dog_friendly=False,
                description="Unique boardwalk trail through swampy terrain with educational signage.",
            ),
            Trail(
                name="Robert Frost Trail (Amherst Section)",
                distance=5.0,
                lat=42.3805,
                lon=-72.5503,
                alt=400.0,
                surface="dirt",
                difficulty=Difficulty.medium,
                bike_friendly=False,
                dog_friendly=True,
                description="Scenic forest trail honoring the poet Robert Frost, with varied terrain.",
            ),
            Trail(
                name="Holyoke Range State Park Trail",
                distance=7.1,
                lat=42.2958,
                lon=-72.5210,
                alt=1000.0,
                surface="rock",
                difficulty=Difficulty.hard,
                bike_friendly=False,
                dog_friendly=True,
                description="Longer, rugged hike with steep climbs and rewarding summit views.",
            ),
            Trail(
                name="Groff Park Loop",
                distance=1.2,
                lat=42.3736,
                lon=-72.5050,
                alt=95.0,
                surface="paved",
                difficulty=Difficulty.easy,
                bike_friendly=True,
                dog_friendly=True,
                description="Small local park loop, perfect for a quick walk or jog.",
            ),
            Trail(
                name="Mill River Recreation Area Trails",
                distance=2.7,
                lat=42.3577,
                lon=-72.5183,
                alt=130.0,
                surface="dirt",
                difficulty=Difficulty.easy,
                bike_friendly=True,
                dog_friendly=True,
                description="Network of short trails along the river, popular with students.",
            ),
        ]

        for trail in trails:
            session.add(trail)
        session.commit()

    print("Database seeded successfully.")


if __name__ == "__main__":
    seed()
