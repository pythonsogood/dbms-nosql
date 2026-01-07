const { faker } = require("@faker-js/faker");
const mongodb = require("mongodb");
const argon2 = require("argon2");

require("dotenv").config()

function randomIntFromInterval(min, max) { // min and max included
    return Math.floor(Math.random() * (max - min + 1) + min);
}

async function seedDB() {
	const uri = process.env.connection;

	const client = new mongodb.MongoClient(uri);
	const now = new Date();

	await client.connect();

	console.log("connected")

	const db = client.db("online_shopping")

	const categories = [];
	const products = [];
	const users = [];
	const addresses = [];
	const reviews = [];
	const orders = [];

	for (let i = 0; i < 15; i++) {
		const category = {
			_id: new mongodb.ObjectId(),
			name: faker.commerce.department(),
		};

		if (categories.length > 0 && Math.random() > 0.8) {
			const parent_category = categories[randomIntFromInterval(0, categories.length - 1)];

			category.parent_id = parent_category._id;
		}

		categories.push(category);
	}

	for (let i = 0; i < 100; i++) {
		const category = categories[randomIntFromInterval(0, categories.length - 1)];
		const created_at = faker.date.recent();
		const images = [];

		for (let j = 0; j < randomIntFromInterval(1, 3); j++) {
			images.push(faker.image.url());
		}

		const product = {
			category_id: category._id,
			name: faker.commerce.productName(),
			description: faker.commerce.productDescription(),
			price: faker.commerce.price(),
			sku: `${faker.string.alpha({length: 3, casing: "upper"})}-${faker.number.int({min: 1000, max: 9999})}`,
			created_at: created_at,
			quantity: faker.number.int({min: 1, max: 100}),
			quantity_updated_at: faker.date.between({from: created_at, to: now}),
			images: images,
		};

		products.push(product);
	}

	for (let i = 0; i < 100; i++) {
		const firstName = faker.person.firstName();
		const lastName = faker.person.lastName();

		const user = {
			_id: new mongodb.ObjectId(),
			email: faker.internet.email({firstName, lastName}),
			password_hash: await argon2.hash(faker.internet.password()),
			full_name: `${firstName} ${lastName}`,
			phone: faker.phone.number({"style": "international"}),
			role: "customer",
			created_at: faker.date.recent(),
		};

		const country = faker.location.country();
		const city = faker.location.city();

		const user_addresses = [];

		for (let j =  0; j < randomIntFromInterval(1, 2); j++) {
			const address = {
				_id: new mongodb.ObjectId(),
				user_id: user._id,
				country: country,
				city: city,
				street: faker.location.streetAddress(),
				postal_code: faker.location.zipCode(),
			}

			user_addresses.push(address);
			addresses.push(address);
		}

		for (let j = 0; j < randomIntFromInterval(1, 2); j++) {
			const address = user_addresses[randomIntFromInterval(0, user_addresses.length - 1)];
			const items = [];

			let total_amount = 0;

			let maxDate = user.created_at;

			for (let k = 0; k < randomIntFromInterval(1, 4); k++) {
				const product = products[randomIntFromInterval(0, products.length - 1)];

				if (product.created_at > maxDate) {
					maxDate = product.created_at;
				}

				total_amount += product.price;

				const item = {
					product_id: product._id,
					quantity: randomIntFromInterval(1, 5),
					price: product.price,
				}

				items.push(item);
			}

			const created_at = faker.date.between({from: maxDate, to: now})

			for (let k = 0; k < items.length; k++) {
				if (Math.random() > 0.8) {
					const item = items[k];

					const review = {
						_id: new mongodb.ObjectId(),
						user_id: user._id,
						product_id: item._id,
						rating: faker.number.int({min: 1, max: 5}),
						comment: faker.lorem.sentences(randomIntFromInterval(1, 3)),
						created_at: faker.date.between({from: created_at, to: now}),
					};

					reviews.push(review);
				}
			}

			const status = Math.random() > 0.33 ? "pending" : "delivered";

			const order = {
				_id: new mongodb.ObjectId(),
				user_id: user._id,
				address_id: address,
				status: status,
				total_amount: total_amount,
				created_at: created_at,
				items: items,
				payment_method: Math.random() > 0.5 ? "paypal" : "card",
				payment_status: status == "delivered" ? "paid" : Math.random() > 0.5 ? "paid" : "unpaid",
				payment_date: faker.date.between({from: created_at, to: now}),
			};

			orders.push(order);
		}

		users.push(user);
	}

	console.log("generated")

	await db.collection("users").insertMany(users);

	await db.collection("addresses").insertMany(addresses);

	await db.collection("categories").insertMany(categories);

	await db.collection("products").insertMany(products);

	await db.collection("reviews").insertMany(reviews);

	await db.collection("orders").insertMany(orders);

	console.log("inserted")

	await client.close();
}

seedDB();