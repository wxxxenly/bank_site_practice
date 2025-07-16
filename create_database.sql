-- public.users определение

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	customer_id int4 GENERATED ALWAYS AS IDENTITY NOT NULL,
	first_name varchar(20) NOT NULL,
	second_name varchar(20) NOT NULL,
	passport_number varchar(20) NOT NULL,
	phone varchar(20) NULL,
	email varchar(50) NULL,
	address varchar(50) NULL,
	CONSTRAINT customers_pk PRIMARY KEY (customer_id)
);


-- public.deposit_transactions определение

-- Drop table

-- DROP TABLE public.deposit_transactions;

CREATE TABLE public.deposit_transactions (
	transaction_id int8 NOT NULL,
	deposit_id int8 NOT NULL,
	transaction_date date NOT NULL,
	transaction_type varchar(25) NOT NULL,
	amount numeric NOT NULL,
	CONSTRAINT deposit_transaction_pk PRIMARY KEY (transaction_id)
);


-- public.interest_accruals определение

-- Drop table

-- DROP TABLE public.interest_accruals;

CREATE TABLE public.interest_accruals (
	accrual_id int8 NOT NULL,
	deposit_id int8 NOT NULL,
	accrual_date date NOT NULL,
	interest_amount numeric NOT NULL,
	CONSTRAINT interest_accruals_pk PRIMARY KEY (accrual_id)
);


-- public.deposit_types определение

-- Drop table

-- DROP TABLE public.deposit_types;

CREATE TABLE public.deposit_types (
	deposit_type_id int8 NOT NULL,
	"name" varchar(20) NOT NULL,
	interest_rate numeric NOT NULL,
	minimum_amount numeric NOT NULL,
	term_months int4 NOT NULL,
	is_replenishable bool NOT NULL,
	is_withdrawable bool NOT NULL,
	CONSTRAINT deposit_types_pk PRIMARY KEY (deposit_type_id)
);


-- public.deposits определение

-- Drop table

-- DROP TABLE public.deposits;

CREATE TABLE public.deposits (
	deposit_id int8 NOT NULL,
	customer_id int4 NOT NULL,
	deposite_type_id int8 NOT NULL,
	amount numeric NOT NULL,
	open_date date NOT NULL,
	close_date date NULL,
	status varchar(20) NOT NULL,
	CONSTRAINT deposits_pk PRIMARY KEY (deposit_id)
);