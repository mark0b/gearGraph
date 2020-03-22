from application import db, gearDb

for piece in gearDb.query.all():
    db.session.delete(piece)
db.session.commit()

print(gearDb.query.all())