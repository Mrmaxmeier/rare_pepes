$(".ui.checkbox").checkbox();

var p1_loader_timeout;
var p2_loader_timeout;

var pepe_queue = [];
var preload = 5;
var max_queue_size = 7;

function next_pepes() {
	console.log("setting pepes", pepe_queue[0])

	// p1_loader_timeout = setTimeout(function(){
	// 	$("#p1dimmer").addClass("active")
	// }, 500);
	// p2_loader_timeout = setTimeout(function(){
	// 	$("#p2dimmer").addClass("active")
	// }, 500);

	$("#p1").attr("src", pepe_queue[0][0])
	$("#p2").attr("src", pepe_queue[0][2])
}

function preload_pepes(data) {
	$("<img />").attr("src", data[0]);
	$("<img />").attr("src", data[2]);
}

function process_pepes(data) {
	if (pepe_queue.length >= max_queue_size) {
		console.log("max pepe queue size exceeded:", pepe_queue.length)
		return
	}
	data[0] = data[0].replace("http://", "//")
	data[2] = data[2].replace("http://", "//")
	console.log("processing pepes", data)
	preload_pepes(data)
	pepe_queue.push(data)
}

$("#p1").on("click", function() {vote("p1")})
$("#p2").on("click", function() {vote("p2")})

// $("#p1").bind("load", function() {
// 	$("#p1dimmer").removeClass("active")
// 	clearTimeout(p1_loader_timeout)
// })

// $("#p2").bind("load", function() {
// 	$("#p2dimmer").removeClass("active")
// 	clearTimeout(p2_loader_timeout)
// })

$(document).keypress(function(e) {
	switch (e.which) {
		case 97:
			//a
			vote("p1")
			break;
		case 100:
			//d
			vote("p2")
			break;
	}
});

function vote(pepe) {
	if (pepe_queue.length < 3) {
		console.log("loading emergency pepes...")
		$.post("/api/get_pepes", {}, process_pepes)
		$.post("/api/get_pepes", {}, process_pepes)
	}
	if (pepe_queue.length < 2) {
		console.log("not enough emergency pepes...")
		return
	}
	switch (pepe) {
		case "p1":
			var uuid = pepe_queue[0][1];
			break
		case "p2":
			var uuid = pepe_queue[0][3];
			break
	}
	pepe_queue.splice(0, 1);
	next_pepes()
	console.log("voting for", uuid)
	console.log("queue size:", pepe_queue.length)
	$("#votes").attr("data-votes", parseInt($("#votes").attr("data-votes")) + 1)
	$("#votes").text($("#votes").attr("data-votes") + " votes on record")
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/api/vote/'+uuid, true);
	xhr.send(null);
	xhr.onreadystatechange = function(e) {
		if (xhr.response) {
			var data = JSON.parse(xhr.response)
			xhr.abort()
			process_pepes(data)
		}
	}
}

$.post("/api/get_pepes", {}, function (data) {
	process_pepes(data)
	next_pepes()
})

for (var i = 0; i < preload-1; i++) {
	$.post("/api/get_pepes", {}, process_pepes)
};
