from lxml import html
import requests
import os
import urllib
import MySQLdb
mysqlUserName = "<SET THIS VALUE>"
mysqlPassword = "<SET THIS VALUE>"
mysqlLocation = "127.0.0.1" # Set this to something else if you're not working locally
cnx = MySQLdb.connect(host=mysqlLocation, port=3306, user=mysqlUserName, passwd=mysqlPassword, db="trails")
c = cnx.cursor()
c.execute("USE trails")
cnx.commit()

page = requests.get('http://www.traildamage.com/trails/index.php')
tree = html.fromstring(page.content)
# buyers = tree.xpath('//a[@href="index.php?id=147"]')

add_trail = ("INSERT INTO trails.trail"
             "(name,county,state,low_end,high_end,rock_crawling,dirt_mud,water_crossing,playgrounds,cliffs_ledges,climbs_descents,elevation,scenery,other,trail_type,season,length,low_point_elevation,high_point_elevation,elevation_change,image_location,image_count,trail_url) "
             "VALUES (%(name)s, %(county)s, %(state)s, %(low_end)s, %(high_end)s, %(rock_crawling)s, %(dirt_mud)s, %(water_crossing)s, %(playgrounds)s, %(cliffs_ledges)s, %(climbs_descents)s, %(elevation)s, %(scenery)s, %(other)s, %(trail_type)s, %(season)s, %(length)s, %(low_point_elevation)s, %(high_point_elevation)s, %(elevation_change)s, %(image_location)s, %(image_count)s, %(trail_url)s)")

for link in tree.xpath('//a'):
    if "id=" in link.attrib['href']:
        trailUrl = 'http://www.traildamage.com/trails/' + link.attrib['href']
        trail = requests.get(trailUrl)
        trailTree = html.fromstring(trail.content)
        firstPTag = trailTree.xpath('//html/body/table/tr/td/div/table/tr/td/p')[0]
        trailName = firstPTag.getchildren()[0].text
        trailNameToSave = str(trailName)
        alreadyExist = c.execute("SELECT * FROM trails.trail WHERE name = '" + trailName + "'")
        cnx.commit()

        # This stops me from creating duplicates.
        # TODO Allow user to overwrite existing data
        if alreadyExist == long(1):
            continue

        location = firstPTag.getchildren()[2].text
        county = location.split(", ")[0]
        state = location.split(", ")[1]
        legend = trailTree.xpath('//td[@class="legend"]/table/tr')

        low_end = legend[0].getchildren()[1].getchildren()[0].text

        high_end = legend[1].getchildren()[1].getchildren()[0].text

        rock_crawling = len(legend[2].getchildren()[1].getchildren())

        dirt_mud = len(legend[3].getchildren()[1].getchildren())

        water_crossing = len(legend[4].getchildren()[1].getchildren())

        playgrounds = len(legend[5].getchildren()[1].getchildren())

        cliffs_ledges = len(legend[6].getchildren()[1].getchildren())

        climbs_descents = len(legend[7].getchildren()[1].getchildren())

        elevation = len(legend[8].getchildren()[1].getchildren())

        scenery = len(legend[9].getchildren()[1].getchildren())

        other = len(legend[10].getchildren()[1].getchildren())

        trail_type = "n/a"
        length = 0.0
        season = "n/a"
        low_point_elevation = 0
        high_point_elevation = 0
        elevation_change = high_point_elevation - low_point_elevation
        secondPTag = trailTree.xpath('//html/body/table/tr/td/div/table/tr/td/p')[1]
        for child in secondPTag.getchildren():
            if child.text is not None:
                if 'Trail Type' in child.text:
                    trail_type = child.getnext().text

                if 'Length' in child.text:
                    length = float(child.tail.split(' miles')[0])

                if 'Season' in child.text:
                    season = child.tail

                if 'Elevation' in child.text:
                    elevationText = child.tail.replace(" feet", "").replace(",", "")
                    low_point_elevation = int(elevationText.split(" to ")[0])
                    try:
                        highPointText = elevationText.split(" to ")[1]
                        if highPointText is not None:
                            high_point_elevation = int(highPointText)
                            elevation_change = high_point_elevation - low_point_elevation
                    except IndexError:
                        print "error while getting high point elevation: " + trailName


        # Getting Images
        baseImagePackage = "images/"
        if not os.path.exists(baseImagePackage):
            os.makedirs(baseImagePackage)
        if trailName.startswith("The "):
            trailName = trailName.split("The ")[1]
        if "Carnage Canyon (BV)" in trailName:
            trailName = 'bv_carnage/'
        trailImageDirectoryLocation = trailName.replace(".", "").replace("'","").replace("The ", "").replace(" ", "_").lower()
        imageDirectoryLocation = requests.get('http://www.traildamage.com/trails/' + trailImageDirectoryLocation)
        imageDirectoryTree = html.fromstring(imageDirectoryLocation.content)
        image_directory_location = baseImagePackage + trailImageDirectoryLocation
        imageCount = 0
        for imageDirectoryLink in imageDirectoryTree.xpath('//a'):
            if imageDirectoryLink.text is not None:
                if ' Parent Directory' not in imageDirectoryLink.text and 'maps/' not in imageDirectoryLink.text and 'thumbnails' not in imageDirectoryLink.text:
                    imageLocation = requests.get('http://www.traildamage.com/trails/' + trailImageDirectoryLocation + '/' +
                                                 imageDirectoryLink.attrib['href'])
                    imageTree = html.fromstring(imageLocation.content)
                    for imageLink in imageTree.xpath('//a'):
                        if imageLink.text is not None:
                            if 'Parent Directory' not in imageLink.text:
                                tripImageDirectoryLocation = baseImagePackage + trailImageDirectoryLocation + "/" + imageDirectoryLink.text.replace(
                                    " ", "")
                                if not os.path.exists(baseImagePackage + trailImageDirectoryLocation):
                                    os.makedirs(baseImagePackage + trailImageDirectoryLocation)
                                if not os.path.exists(tripImageDirectoryLocation):
                                    os.makedirs(tripImageDirectoryLocation)
                                imageSaveLocation = tripImageDirectoryLocation + imageLink.attrib['href']
                                if not os.path.exists(imageSaveLocation):
                                    image = urllib.URLopener().retrieve(
                                        'http://www.traildamage.com/trails/' + trailImageDirectoryLocation + '/' +
                                        imageDirectoryLink.attrib['href'] + imageLink.attrib['href'], imageSaveLocation)
                                imageCount += 1

        trail = {
            'name': trailNameToSave,
            'county': county,
            'state': state,
            'low_end': low_end,
            'high_end': high_end,
            'rock_crawling': rock_crawling,
            'dirt_mud': dirt_mud,
            'water_crossing': water_crossing,
            'playgrounds': playgrounds,
            'cliffs_ledges': cliffs_ledges,
            'climbs_descents': climbs_descents,
            'elevation': elevation,
            'scenery': scenery,
            'other': other,
            'trail_type': trail_type,
            'season': season,
            'length': length,
            'low_point_elevation': low_point_elevation,
            'high_point_elevation': high_point_elevation,
            'elevation_change': elevation_change,
            'image_location': image_directory_location,
            'trail_url': trailUrl,
            'image_count': imageCount,
        }

        c.execute(add_trail, trail)
        cnx.commit()
        print "Trail Name: " + trailName
c.close()
cnx.close()

