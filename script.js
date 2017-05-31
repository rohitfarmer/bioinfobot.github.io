
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
	var imageInsert = '<img id="wordcloud"'+'src='+'"'+imagePath+'"'+'OnError="this.src=\'images\/default.png\'\;"'+'>';
	//document.write(imageInsert)
	document.getElementById("wordcloud").innerHTML = imageInsert;		
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
}

