<?php
$type = $_POST['type'];

$con = mysqli_connect("den1.mysql2.gear.host","econsave","Qh7CDqjHd!-a", "econsave");
if (mysqli_connect_errno($con)) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

if ($type == 1){
	$news_name = ($_POST['n']);
	$news_date = ($_POST['d']);
	$news_link = ($_POST['l']);
	
	$control = true;
	$query2 = "select news_link from news;";
	$result2 = mysqli_query($con, $query2) or die(mysqli_error($con));
	if(!$result2)
	{
		echo 'Empty locations' . mysqli_error();
	}
	else
	{
		if(mysqli_num_rows($result2) != 0)
		{
			while($row = mysqli_fetch_assoc($result2))
			{
				if ($row['news_link'] == $news_link){
					$control = false;
				}
			}
		}
	}
	if ($control == true){
		$query = "insert into news(news_name, news_date, news_link) values ('$news_name', '$news_date', '$news_link');";
		mysqli_query($con, $query) or die(mysqli_error($con));
		echo "News Uploaded:";
	}else{
		echo "News Already Uploaded:";
	}
}elseif($type == 2){
	$share_price = ($_POST['p']);
	$share_date = ($_POST['d']);
	$share_market = ($_POST['m']);
	
	$control = true;
	$query2 = "select share_date, share_price from stock;";
	$result2 = mysqli_query($con, $query2) or die(mysqli_error($con));
	if(!$result2)
	{
		echo 'Empty locations' . mysqli_error();
	}
	else
	{
		if(mysqli_num_rows($result2) != 0)
		{
			while($row = mysqli_fetch_assoc($result2))
			{
				if ($row['share_date'] == $share_date and $row['share_price'] == $share_price){
					$control = false;
				}
			}
		}
	}
	if ($control == true){
		$query = "insert into stock(share_date, share_price, share_market) values ('$share_date', '$share_price', '$share_market');";
		mysqli_query($con, $query) or die(mysqli_error($con));
		echo "Stock Uploaded:";#
	}else{
		echo "Stock Already Uploaded:";
	}
}

mysqli_close($con);
?>