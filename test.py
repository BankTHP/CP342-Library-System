id = 62102010169
name = "ธนพัฒน์"
lastname = "เอี่ยมประเสริฐ"
major = "วิทยาการคอมพิวเตอร์"
year = "2"
excuteStr = ("UPDATE student SET std_firstname = '"'{}'"' , std_lastname = '"'{}'"' , std_major = '"'{}'"' , std_year= '"'{}'"' WHERE std_id = {};").format(name,lastname,major,year,id)
print(excuteStr)