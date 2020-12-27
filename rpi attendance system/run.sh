INPUT_STRING=0
while [ "$INPUT_STRING" != 5 ]
do
echo "==================Welcome To Attendance Syatem=========================="
echo "1.create new student database"
echo "2.capture live image"
echo "3.Mark attedance"
echo "4.See attendance"
echo "5.Exit"

  read INPUT_STRING
  case $INPUT_STRING in
	1)
		sudo python create_database.py
		;;
	2)
		sudo python capture_group.py
		;;
	3)
		sudo python create_attendance.py
		;;
	4)
		sudo python see_attendance.py
		;;
	5)	
		INPUT_STRING=5
		break
		;;
	6)
		echo "Sorry, I don't understand"
		break
		;;
  esac
done
