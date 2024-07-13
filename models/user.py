from mr_config import  mr_init as mr
class User(mr.Model):
    __tablename__='userlo'
    username = mr.Column(mr.String(255), primary_key=True, nullable=False)
    email = mr.Column(mr.String(255), nullable=False)
    gender = mr.Column(mr.String(255), nullable=False)
    password = mr.Column(mr.String(255), nullable=False)


    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'gender': self.gender,
            'password': self.password
        }
