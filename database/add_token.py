import datetime
from sqlalchemy.orm import Session
from database.db import engine, Token


def add_token_to_base(eth_token, eth_url, weth):
    session = Session(bind=engine)
    new_token: Token = Token(
        date=datetime.datetime.now(),
        token=eth_token,
        token_url=eth_url,
        weth=weth,
        score='')
    with session:
        session.add(new_token)
        session.commit()
        