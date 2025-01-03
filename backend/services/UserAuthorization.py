class UserAuthorization:

    def login(db_name, nickname, password):
        pass

    def registaration(db_name, db, name, nickname, password) -> bool:
        if UserAuthorization.unique_data(db_name, nickname):
            return False
        users = db_name(name=name, nickname=nickname, password=password)
        db.session.add(users)
        db.session.flush()
        db.session.commit()
        return True

    def data_is_true(db_name, nickname, password):
        return "45"

    def unique_data(db_name, nickname):
        if db_name.query.filter_by(nickname=nickname).first():
            return False
        else:
            return True