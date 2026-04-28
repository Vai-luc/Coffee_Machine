class Car:
    def __init__(self,model,year,color,for_sale):
        self.model = model
        self.year = year
        self.color = color
        self.for_sale = for_sale

car1= Car("Mustang",2024,"Red",False)
car2= Car("Corvette",2025,"Blue",True)
car3= Car("Charger",2026,"Yellow",True)

Cars = [car1,car2,car3]
for c in Cars:
    print(c)
