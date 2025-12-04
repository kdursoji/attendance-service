from sqlalchemy import Column, Integer, DateTime, String, func

from datastore.base_class import Base


class ProfileImages(Base):
    __tablename__ = 'profile_images_t'
    id = Column("id", Integer, primary_key=True)
    image_location = Column("image_location", String(250), nullable=False)
    created_on = Column("created_on", DateTime(timezone=True), nullable=False, default=func.now())

    def serialize(self):
        data = {
            "id": self.id,
            "image_location": self.image_location
        }
        return data
