<?php
$con = mysqli_connect("den1.mysql2.gear.host","econsave","", "econsave");
if (mysqli_connect_errno($con)) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

 header('Content-Type: application/json');

    $aResult = array();
	$var = "";

    if( !isset($_POST['functionname']) ) { $aResult['error'] = 'No function name!'; }

    if( !isset($_POST['arguments']) ) { $aResult['error'] = 'No function arguments!'; }

    if( !isset($aResult['error']) ) {
        switch($_POST['functionname']) {
            case 'stocks':
				$query2 = "select * from stock ORDER BY share_date DESC;";
				$result2 = mysqli_query($con, $query2) or die(mysqli_error($con));
				if(!$result2)
				{
				   echo 'Empty' . mysqli_error();
				}
				else
				{
					if(mysqli_num_rows($result2) != 0)
					{
						while($row = mysqli_fetch_assoc($result2))
						{
							$dateObject = DateTime::createFromFormat("Y-m-d", $row['share_date']);
							$var .= $dateObject->format('d/m/Y');
							$var .=  "---";
							$var .=  $row['share_price'];
							$var .=  "---";
							$var .=  $row['share_market'];
							$var .=  ";";
						}
					}
				}
				$aResult['result'] = $var;
				break;
			   
			case 'news':
				$query2 = "select * from news ORDER BY news_date DESC;";
				$result2 = mysqli_query($con, $query2) or die(mysqli_error($con));
				if(!$result2)
				{
				   echo 'Empty' . mysqli_error();
				}
				else
				{
					if(mysqli_num_rows($result2) != 0)
					{
						while($row = mysqli_fetch_assoc($result2))
						{
							$dateObject = DateTime::createFromFormat("Y-m-d", $row['news_date']);
							$var .= $dateObject->format('d/m/Y');
							$var .=  "---";
							$var .=  $row['news_name'];
							$var .=  "---";
							$var .=  $row['news_link'];
							$var .=  ";";
						}
					}
				}
				$aResult['result'] = $var;
				break;
        }

    }
	
	echo json_encode($aResult);
	

?>
