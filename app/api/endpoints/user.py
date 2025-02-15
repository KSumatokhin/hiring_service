from fastapi import APIRouter

from app.core.user import auth_backend
from app.crud.user import fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)

# @router.post("/register/")
# async def register_user(user_data: SUserRegister) -> dict:
#     user = await UsersDAO.find_one_or_none(email=user_data.email)
#     if user:
#         raise UserAlreadyExistsException
#     user_dict = user_data.dict()
#     user_dict['password'] = get_password_hash(user_data.password)
#     await UsersDAO.add(**user_dict)
#     return {'message': f'Вы успешно зарегистрированы!'}
#
#
# @router.post("/login/")
# async def auth_user(response: Response, user_data: SUserAuth):
#     check = await authenticate_user(email=user_data.email, password=user_data.password)
#     if check is None:
#         raise IncorrectEmailOrPasswordException
#     access_token = create_access_token({"sub": str(check.id)})
#     response.set_cookie(key="users_access_token", value=access_token, httponly=True)
#     return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}
#
#
# @router.post("/logout/")
# async def logout_user(response: Response):
#     response.delete_cookie(key="users_access_token")
#     return {'message': 'Пользователь успешно вышел из системы'}
#
#
# @router.get("/me/")
# async def get_me(user_data: User = Depends(get_current_user)):
#     return user_data
#
#
# @router.get("/all_users/")
# async def get_all_users(user_data: User = Depends(get_current_admin_user)):
#     return await UsersDAO.find_all()