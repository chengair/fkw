@echo off

call sqlite3 fkw.db
delete from keywords;
.import keywords.txt keywords
select count(1) from keywords;
pause
