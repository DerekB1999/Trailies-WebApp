from fastapi import FastAPI, Query, status, Form, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel
from database import engine, get_session
from schemas import Password, Difficulty
from sqlmodel import Session, select
from models import User, Trail, TrailReview
from security import hash_password, verify_password, create_access_token
from typing import Optional
from dependencies import get_current_user

app = FastAPI(title='Trailies', version='1.0.2')


app.mount('/static', StaticFiles(directory='static'),
          name='static')  # Mount the static files

# Setup the Jinja2 templates
templates = Jinja2Templates(directory='templates')

# Create the database tables
SQLModel.metadata.create_all(engine)


# If user goes to / URL, will be redirected to login
@app.get('/', response_class=HTMLResponse)
async def root():
    return RedirectResponse(url='/signup')


# Sign up starts here
@app.post('/signup', response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def create_user(first_name: str = Form(...), last_name: str = Form(...), username: str = Form(...),
                      email: str = Form(...), password: Password = Form(...), session: Session = Depends(get_session)):

    # Remove extra spaces around the strings
    first_name = first_name.strip()
    last_name = last_name.strip()
    username = username.strip()
    email = email.strip()

    username_taken = session.exec(select(User).where(
        User.username == username)).first()

    email_taken = session.exec(select(User).where(User.email == email)).first()

    if username_taken:
        return """
          <div class='error-message'>
            Username already exists
          </div>
        """

    if email_taken:
        return """
          <div class='error-message'>
            Email already exists
          </div>
        """

    user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        hashed_password=hash_password(password)
        # Role defaults to user in model, not needed
    )

    session.add(user)
    session.commit()
    session.refresh(user)  # Gives user an auto generated ID
    return """
      <div>
        Account created! Redirecting to login!
      </div>
      <script>
        setTimeout(() => window.location.href = '/login', 1000)
      </script>
    """


@app.get('/signup', response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name='signup.html')


@app.post('/login', response_class=HTMLResponse)
async def login(session: Session = Depends(get_session), username: str = Form(...), password: Password = Form(...)):
    username = username.strip()
    user = session.exec(select(User).where(User.username == username)).first()

    if not user or not verify_password(password, user.hashed_password):
        return """
          <div id="login-error" class="error-message">
            Invalid username or password
          </div>
        """

    # If login is successful, create a token
    access_token = create_access_token(data={'sub': user.username})

    response = HTMLResponse("""
        <div>
          Login successful!              
        </div>
        <script>
          setTimeout(() => window.location.href='/homepage')           
        </script>
      """)

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=True,  # Switch to true in production
        samesite='lax'
    )

    return response


@app.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')


@app.get('/signout')
async def signout():
    response = RedirectResponse('/login')
    response.delete_cookie('access_token')
    return response


@app.get('/homepage', response_class=HTMLResponse)
async def homepage(request: Request, user: Optional[User] = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url='/login', status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(request=request, name='homepage.html', context={'user': user})


@app.post('/trails/new', response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def add_trails(name: str = Form(...), distance: float = Form(...), lat: float = Form(...),
                     lon: float = Form(...), alt: Optional[float] = Form(None), surface: str = Form(...),
                     difficulty: Difficulty = Form(...), bike_friendly: bool = Form(False),
                     dog_friendly: bool = Form(False), description: Optional[str] = Form(None),
                     session: Session = Depends(get_session), user: User = Depends(get_current_user)):

    if user.role != 'admin':
        raise HTTPException(status_code=403, detail='Admins only')

    trail = Trail(
        name=name,
        distance=distance,
        lat=lat,
        lon=lon,
        alt=alt,
        surface=surface,
        difficulty=difficulty,
        bike_friendly=bike_friendly,
        dog_friendly=dog_friendly,
        description=description
    )

    session.add(trail)
    session.commit()
    session.refresh(trail)
    return f"""
      <div>
        {trail.name} added successfully!
      </div>
      <script>
        setTimeout(() => window.location.href = '/trails')
      </script>
    """


@app.get('/trails/new', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def new_trail_page(request: Request, user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url='/login', status_code=status.HTTP_302_FOUND)
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail='Admins only')

    return templates.TemplateResponse(request=request, name='trail_new.html')


@app.get('/trails', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def trails_list(request: Request, user: Optional[User] = Depends(get_current_user),
                      session: Session = Depends(get_session)):
    if user is None:
        raise HTTPException(status_code=401, detail='Please sign in!')

    trails = session.exec(select(Trail).order_by(Trail.name)).all()
    all_reviews = session.exec(select(TrailReview)).all()

    avg_ratings = {}
    for trail in trails:
        trail_reviews = [
            r for r in all_reviews if r.trail_id == trail.trail_id]
        avg_ratings[trail.trail_id] = round(sum(
            r.rating for r in trail_reviews) / len(trail_reviews), 1) if trail_reviews else None

    return templates.TemplateResponse(request=request, name='fragments/trails_list.html', context={'trails': trails, 'user': user, 'avg_ratings': avg_ratings})


@app.get('/trails/difficulty', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def filter_trail_difficulty(request: Request, session: Session = Depends(get_session), difficulty: Optional[str] = Query(None),
                                  user: User = Depends(get_current_user)):
    if difficulty:
        trails_difficulty = session.exec(
            select(Trail).where(Trail.difficulty == difficulty)).all()
    else:
        trails_difficulty = session.exec(
            select(Trail).order_by(Trail.name)).all()

    all_reviews = session.exec(select(TrailReview)).all()
    avg_ratings = {}
    for trail in trails_difficulty:
        trail_reviews = [
            r for r in all_reviews if r.trail_id == trail.trail_id]
        avg_ratings[trail.trail_id] = round(sum(
            r.rating for r in trail_reviews) / len(trail_reviews), 1) if trail_reviews else None

    return templates.TemplateResponse(request=request, name='fragments/filtered_list.html', context={'trails': trails_difficulty, 'user': user, 'avg_ratings': avg_ratings})


@app.get('/trails/{trail_id}', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def trail_details(request: Request, trail_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    trail = session.exec(select(Trail).where(
        Trail.trail_id == trail_id)).first()
    if trail is None:
        raise HTTPException(status_code=404, detail='Trail not found')

    reviews = session.exec(select(TrailReview).where(
        TrailReview.trail_id == trail_id)).all()
    if reviews:
        avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1)
    else:
        avg_rating = None

    return templates.TemplateResponse(request=request, name='trail_detail.html', context={'trail': trail, 'user': user,
                                                                                          'avg_rating': avg_rating})


@app.delete('/trails/{trail_id}/delete')
async def delete_trail(trail_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail='Admins only')

    trail = session.get(Trail, trail_id)

    if trail is None:
        raise HTTPException(status_code=404, detail='Trail not found')

    session.delete(trail)
    session.commit()

    # This will replace the li with an empty space, therefore it'll disappear
    return ''


@app.post('/trails/{trail_id}/reviews', response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def add_review(request: Request, trail_id: int, rating: int = Form(...), comment: Optional[str] = Form(None),
                     session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    trail = session.get(Trail, trail_id)
    if not trail:
        raise HTTPException(status_code=404, detail='Trail not found')

    if user.user_id is None:
        raise HTTPException(status_code=404, detail='Trail not found')

    review = TrailReview(
        trail_id=trail_id,
        user_id=user.user_id,
        rating=rating,
        comment=comment
    )
    session.add(review)
    session.commit()
    session.refresh(review)

    return f"""
      <li>
        Posted by: {user.first_name} {user.last_name}<br>
        <p>Rating: {review.rating}</p>
        <p>Comment: {review.comment}</p>
        <p>Posted: {review.created_at.strftime('%B %d, %Y')}</p>
      </li>
    """


@app.get('/trails/{trail_id}/reviews', response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def reviews_list(request: Request, trail_id: int, session: Session = Depends(get_session),
                       user: User = Depends(get_current_user)):
    reviews = session.exec(select(TrailReview).where(
        TrailReview.trail_id == trail_id)).all()

    reviewer_ids = {r.user_id for r in reviews}
    reviewers = {u.user_id: u for u in session.exec(
        select(User).where(User.user_id.in_(reviewer_ids))).all()}

    return templates.TemplateResponse(request=request, name='fragments/reviews_list.html',
                                      context={'reviews': reviews, 'reviewers': reviewers, 'user': user})
