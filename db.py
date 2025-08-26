import csv
from application import gearDb, db
from sys import argv, stderr, stdout
from application import gearDb, db, Rack, association


def clearDb():
    for piece in gearDb.query.all():
        db.session.delete(piece)
    db.session.commit()


def messDb():
    mine = db.session.query(Rack.name).filter(Rack.name == "myRack").all()
    print(mine)


def showHelp(file=stdout):
    print("naw")


def loadData(file_name):
    return list(csv.reader(open(file_name)))


def fillDb():
    file_name = "static/gear.csv"
    data = loadData(file_name)
    data.pop(0)  # Remove the header
    for i in data:  # loop through rows of the csv and fill the db.
        record = gearDb(
            brand=i[1],
            current=bool(i[0]),
            sizeCode=i[2],
            color=i[3],
            lobes=1 if i[4] == 'N/A' else int(i[4]),
            weightG=float(i[5]) if i[5] != '' else 0,
            strengthKn=float(i[6]) if i[6] != '' else 0,
            fullName=i[7],
            lowFitMm=float(i[8]) if i[8] != '' else 0,
            upFitMm=float(i[9]))
        db.session.add(record)
    db.session.commit()

    everything = gearDb.query.all()
    print(len(everything), type(everything))


def populateDb():
    # file_name = "static/gear.csv"
    # data = loadData(file_name)
    # print(type(data),len(data),len(data[1]))
    # print(data[1])
    fillDb()


handlers = {
    "--help": showHelp,
    "clear": clearDb,
    "mess": messDb,
    "populate": populateDb,
}


try:
    handler = handlers[argv[1]]
except:
    showHelp(file=stderr)

handler()
