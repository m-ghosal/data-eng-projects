'''
Program that analyzes whether Sakila is appropriately stocked.
'''
import sqlite3
import pandas as pd

#TODO fill in
def connect(filename):
	'''Returns a connection to the Sakila database refered
	   by the provided file name
	'''
	con = sqlite3.connect(filename)
	return con


#TODO fill in
def inventory_dataset(con):
	'''Returns a pandas dataframe where each row is a film and 
	   with the following attributes:
	   	* film name
	   	* number of copies in the inventory
	   	* number of times the film has been rented out
	   	* rental price
	   	* replacement pice
	'''
	query1 = '''SELECT COUNT(inventory.film_id) FROM film, inventory WHERE film.film_id = inventory.film_id GROUP BY film.title;
	'''
	query2 = '''SELECT film.title, COUNT(rental.rental_id), film.rental_rate, film.replacement_cost FROM film, inventory, rental
	WHERE film.film_id = inventory.film_id AND inventory.inventory_id = rental.inventory_id GROUP BY film.title;'''
	data1 = con.execute(query1)
	data2 = con.execute(query2)
	name_arr =[]
	num_copies_arr = []
	num_rent_arr = []
	rental_price = []
	replacement_price = []
	for row in data1:
		num_copies_arr.append(row[0])
	for row in data2:
		name_arr.append(row[0])
		num_rent_arr.append(row[1])
		rental_price.append(row[2])
		replacement_price.append(row[3])
	query_df = pd.DataFrame({'name' : name_arr, 'inv_copies' : num_copies_arr, 'rentals' : num_rent_arr, 'rental_rate' : rental_price, 'replacement_price' : replacement_price})
	return query_df


con = connect('sqlite-sakila.db')
df = inventory_dataset(con)
df.to_csv('inventory_dataset.csv')



