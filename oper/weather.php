<?php

	$plyrid=$_POST['GSOD2018'];
	echo $plyrid; 
	if (isset($_POST['Submit'])) {
		echo "<table><tr><th>station</th><th>Temp_max</th><th>Temp_min</th><th>Temp_avg</th></tr>";
		
		$sql="SELECT station, temp_max, temp_min, temp_avg FROM GSOD2018 = '$plyrid'";
		/*result=$conn->query("SELECT station, temp_max, temp_min, temp_avg FROM GSOD2018 WHERE station = '$plyrid' ORDER BY temp_max DESC"); */
		$result = $conn -> query($sql);
		if ($result->num_rows > 0) {
			while($row=$result->fetch_assoc()) {
				echo "<tr><td>" .$row["station"]. "</td><td>" .$row["Temp_max"]. "</td><td>" .$row["Temp_min"]. "</td><td>" .$row["Temp_avg"]. "</td></tr>";
			}
		}
			else {
				echo "Nothing";
			}
				echo "</table>";
	}
?>

<h1>Figure 2: Latitude and Longitude on Weather Stations</h1>
<img src="images/Figure_2(a).png" alt="LatandLong" weight=400px height=250px> <br>
<img src="images/Figure_2(b).png" alt="Maxandmin" weight=400px height=250px> <br>

<?php

<?php

	$plyrid=$_POST['GSOD2018'];
	echo $plyrid; 
	if (isset($_POST['Submit'])) {
		echo "<table><tr><th>station</th><th>Latitude</th><th>Longitude</th></tr>";
		
		$sql="SELECT station, Latitude, Longitude FROM GSOD2018 = '$plyrid'";
		/*result=$conn->query("SELECT station, latitude, longitude FROM GSOD2018 WHERE station = '$plyrid' ORDER BY latitude DESC"); */
		$result = $conn -> query($sql);
		if ($result->num_rows > 0) {
			while($row=$result->fetch_assoc()) {
				echo "<tr><td>" .$row["station"]. "</td><td>" .$row["Latitude"]. "</td><td>" .$row["Longitude"]. "</td></tr>";
			}
		}
			else {
				echo "Nothing";
			}
				echo "</table>";
	}
?>