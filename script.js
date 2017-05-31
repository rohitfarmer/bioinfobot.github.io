
function onloadfunc(){
	var d = new Date();
	var m = d.getUTCMonth();
	var m = m -1;
	var m = ("0" + m).slice(-2);
	var y = d.getUTCFullYear();
	var name = y+'-'+m; 
	//document.write(name);
	var imagePath = "images\/"+name+".png"
	//document.write(imagePath)
	var imageInsert = '<img align="center" id="wordcloud"'+'src='+'"'+imagePath+'"'+'OnError="this.src=\'images\/default.png\'\;"'+'>';
	//document.write(imageInsert)
	document.getElementById("wordcloud").innerHTML = imageInsert;
	monthText = "Analysis results for "+name;
	document.getElementById("month").innerHTML = monthText;		
	//alert('It seems that the bot is still processing results please visit later for latest results.');
		
}

function wrongyear(){
	alert("I can only show data from the past, neither present nor future. \nPlease try again with a previous month.");
	location.reload();
}

function main(yearMonth) {
	var year = yearMonth.year.value;
	var name = yearMonth.year.value+'-'+yearMonth.month.value;
	//var imageInsert = '<img id="wordcloud"'+'src='+"\""+'images\/'+name+'.png'+"\""+'OnError="this.src=\'images\/default.png\'\;"'+'>';
	var imageInsert = '<img id="wordcloud"'+'src='+"\""+'images\/'+name+'.png'+"\""+'OnError="wrongyear\(\)\;"'+'>';
	document.getElementById("wordcloud").innerHTML = imageInsert;
	monthText = "Analysis results for "+name;
	document.getElementById("month").innerHTML = monthText;	
	jsondata(name);
}

// This function mostly uses jQuery
function jsondata(name){
	//alert(name)
	jsonPath = "https\:\/\/bioinfobot\.github\.io\/data\/"+name+".json";
	$.getJSON(jsonPath, function(json) {
    	usersFreq=json.UsersFreq;
		topWords=json.TopWords;
		hashFreq=json.HashFreq;

		$(oneliner).html(json.TweetCount+" tweets were analyzed consisting of "+json.TotalWords+" total words with "+json.UniqueWords+" unique words.");
		$(tCount).html("Total tweets analyzed "+json.TweetCount);
		$(tWords).html("Total words "+json.TotalWords);
		$(uWords).html("Unique words "+json.UniqueWords);

		var userArr=[];
		for (var i=0; i<usersFreq.length; i++) {
			string="\@"+usersFreq[i][0]+" ("+usersFreq[i][1]+"), ";
			userArr.push(string)
			//alert(usersFreq[i]);
		}
		$(uFreq).html(userArr);
	});
}