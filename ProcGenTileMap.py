from opensimplex import OpenSimplex
from reportlab.lib.pagesizes import letter #import necessary for American style page sizes
from reportlab.pdfgen import canvas

#Reads in an array of tiles | currently need to be in same directory as script
tiles = ["testterrain0.png", "testterrain1.png", "testterrain2.png", "testterrain3.png", "testterrain4.png"]

#Number of tiles per page both length and width
MAP_HEIGHT = 8
MAP_WIDTH = 8

# Slide page tiles up or down based on the Map height and width
X_PAGE = 1
Y_PAGE = 1
VERT_OFFSET = MAP_HEIGHT * Y_PAGE
HOR_OFFSET = MAP_WIDTH * X_PAGE

#Size of tiles printed to the page
TILE_WIDTH = 64
TILE_HEIGHT = 64
PAGE_MARGIN = 15
SEED = 1

#Name of file dynamically changes for map coordinates
fileName = ("Map_%s - %s,%s.pdf" %(SEED, X_PAGE, Y_PAGE))
map = canvas.Canvas (fileName, pagesize=letter)

#Initiates OpenSimplex class from SEED using the opensimplex library
gen = OpenSimplex(SEED)

#Generates scaled noise for drawTile function
def noise(nx, ny):

    return gen.noise2(nx, ny) # Generates wave numbers -1.0:+1.0 to 0.0:1.0

#Function that draws tiles onto the PDF
#TODO Print map coordinates in small font for reference
def drawTiles(map, HOR_OFFSET, VERT_OFFSET):

    num = []

    for x in range (MAP_WIDTH):
        num.append([0] * MAP_WIDTH)
        for y in range (MAP_HEIGHT):
            print("x,y: %s, %s" %(x, y)) # For debugging

            #Offset x and y for traversing multiple pages
            ox = x
            oy = y
            ox = x + HOR_OFFSET
            oy = y + VERT_OFFSET
            print("ox,oy: %s, %s" %(ox, oy))  # For debugging
            nx = ox/MAP_WIDTH # '- 0.5 originally added'
            ny = oy/MAP_HEIGHT # '- 0.5 originally added'
            print("nx: %s" %(nx))  # For debugging
            print("ny: %s" %(ny))  # For debugging

            num[x][y] = ((1 * noise(nx, ny))
                          + (0.5 * noise(2 * nx, 2 * ny))
                          + (0.25 * noise(4 * nx, 2 *ny)))
            print("num[x][y]: %s" %(num[x][y]))  # For debugging
            random = getTile(num[x][y])
            map.drawImage(tiles[random], x * TILE_WIDTH + PAGE_MARGIN, y * TILE_HEIGHT + PAGE_MARGIN, width=TILE_WIDTH, height=TILE_HEIGHT)

#Returns a tile based on the tile position in 'tiles' array
#Adjust numbers for different frequencies of terrain based on numbers output between -1.0 to 1.0
def getTile(number):

    tileNumber = 0

    if number < 0.0:
        tileNumber = 0
        return tileNumber
    elif number < 0.5:
        tileNumber = 1
        return tileNumber
    elif number < 0.7:
        tileNumber = 2
        return tileNumber
    elif number < 0.8:
        tileNumber = 3
        return tileNumber
    else:
        tileNumber = 4
        return tileNumber

#Calls draw tile function
drawTiles(map, HOR_OFFSET, VERT_OFFSET)

#Prints images to page and saves
map.showPage()
map.save()
