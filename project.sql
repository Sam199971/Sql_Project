use SQL_Class;
/*
drop table [Space];
drop table SpaceTime;

*/

/*
create table Product(
	pId int Not Null,
	pName varchar(10),
	pNumber int,
	unitPrice int,
	Primary Key (pId)
);

Insert into Product values(1, '大包', 3, 10000)


Insert into Product values(2, '中包', 5, 1000)

Insert into Product values(3, '小包', 7, 100);
Insert into Product values(4, '骰子', 10, 50);
Insert into Product values(5, '台啤(18天)', 50, 100);


create table [User](
	uId int Not Null,
	uName varchar(15),
	Primary Key (uId)
);


create table Trade(
	uId int Not Null,
	tId int Not Null,
	tradeTime Datetime,
	Primary Key (tId),
	FOREIGN KEY (uId) REFERENCES [User](uId) ON UPDATE CASCADE on delete No action 
);

create table Record(
	pId int Not Null,
	tId int Not Null,
	amount int,
	salePrice int,
	CONSTRAINT pId_tId PRIMARY KEY (pId, tId),
	FOREIGN KEY (tId) REFERENCES Trade(tId) ON UPDATE CASCADE on delete No action,
	FOREIGN KEY (pId) REFERENCES Product(pId) ON UPDATE CASCADE on delete No action 
);
*/

/*
create table [Space](
	sId int Not Null,
	sType Varchar(10),
	PricePerHour int,
	PRIMARY KEY (sId)
);

create table SpaceTime(
	[sId] int Not Null,
	[uId] int Not Null,
	[Date] date,
	StartTime time,
	EndTime time,
	TotalTime int,
	TotalPrice int,
	Constraint suId Primary Key([sId], date, StartTime),
	FOREIGN KEY ([sId]) REFERENCES [Space]([sId]) ON UPDATE CASCADE on delete No action,
	FOREIGN KEY ([uId]) REFERENCES [User]([uId]) ON UPDATE CASCADE on delete No action 
);
*/

/*
Insert into [Space] values(1, '小包', 10);
Insert into [Space] values(2, '小包', 10);
Insert into [Space] values(3, '小包', 10);
Insert into [Space] values(4, '小包', 10);
Insert into [Space] values(5, '小包', 10);

Insert into [Space] values(6, '中包', 20);
Insert into [Space] values(7, '中包', 20);
Insert into [Space] values(8, '中包', 20);
Insert into [Space] values(9, '中包', 20);

Insert into [Space] values(10, '大包', 30);
Insert into [Space] values(11, '大包', 30);
Insert into [Space] values(12, '大包', 30);


Insert into SpaceTime values(1, 1, '2021-04-16', '00:00:00', '01:00:00', 1, 10);


Insert into SpaceTime values(1, 1, '2021-04-16', '13:00:00', '14:00:00', 1, 10);



Insert into SpaceTime values(5, 1, '2021-04-16', '01:00:00', '02:00:00', 1, 10);

Insert into SpaceTime values(6, 1, '2021-04-16', '03:00:00', '05:00:00', 2, 40);

Insert into SpaceTime values(10, 1, '2021-04-16', '01:00:00', '02:00:00', 1, 30);

Insert into SpaceTime values(11, 1, '2021-04-16', '11:00:00', '13:00:00', 2, 60);
*/

Select *
		From SpaceTime as ST inner join [Space] as S
		                      on ST.sId = S.[sid]
		Where Date = '2021-04-16'  and S.sType = '';


Select *
		From [Space] as S
		Where S.sType = '小包'




