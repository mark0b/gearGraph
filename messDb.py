from application import gearDb, db, Rack, association
mine = db.session.query(Rack.name).filter(Rack.name == "myRack").all()

print(mine)