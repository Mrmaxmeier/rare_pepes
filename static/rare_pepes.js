$(".ui.checkbox").checkbox();

var pepe_queue = [];
var current_pepes;
var preload = 7;
var max_queue_size = 10;

function next_pepes() {
	current_pepes = pepe_queue[0];
	console.log("setting pepes", current_pepes);

	pepe_queue.splice(0, 1);

	if (!current_pepes[4])
		$("#p1dimmer").addClass("active");
	if (!current_pepes[5])
		$("#p2dimmer").addClass("active");

	$("#p1").attr("src", current_pepes[0]);
	$("#p2").attr("src", current_pepes[2]);
}

function update_status_bar() {
	var loaded = 0;
	for (var i = pepe_queue.length - 1; i >= 0; i--) {
		if (pepe_queue[i][4])
			loaded += 1;
		if (pepe_queue[i][5])
			loaded += 1;
	}
	var progress = loaded / (pepe_queue.length * 2);
	//console.log(status_bar_last, progress);
	if (NProgress.isStarted() || progress < 0.7)
		NProgress.set(progress);
}

NProgress.configure({ showSpinner: false, trickle: false, easing: 'ease', speed: 2500 });
NProgress.start();

function pepe_preloaded(data, pepe) {
	switch (pepe) {
		case "p1":
			data[4] = true;
			if (data == pepe_queue[0])
				$("#p1dimmer").removeClass("active");
			break;
		case "p2":
			data[5] = true;
			if (data == pepe_queue[0])
				$("#p2dimmer").removeClass("active");
	}
	update_status_bar();
}

function preload_pepes(data) {
	$("<img />").attr("src", data[0]).one("load", function() {
		pepe_preloaded(data, "p1");
	}).each(function() {if (this.complete) $(this).load();});
	$("<img />").attr("src", data[2]).one("load", function() {
		pepe_preloaded(data, "p2");
	}).each(function() {if (this.complete) $(this).load();});
}

function process_pepes(data) {
	if (pepe_queue.length >= max_queue_size) {
		console.log("max pepe queue size exceeded:", pepe_queue.length);
		return;
	}
	data[0] = data[0].replace("http://", "//");
	data[2] = data[2].replace("http://", "//");
	console.log("processing pepes", data);
	data.push(false); // is_loaded
	data.push(false);
	preload_pepes(data);
	pepe_queue.push(data);
	update_status_bar();
}

$("#p1").on("click", function() {vote("p1");});
$("#p2").on("click", function() {vote("p2");});

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
			vote("p1");
			break;
		case 100:
			//d
			vote("p2");
			break;
	}
});

function vote(pepe) {
	if (pepe_queue.length < 3) {
		console.log("loading emergency pepes...");
		$.post("/api/get_pepes", {}, process_pepes);
	}
	if (pepe_queue.length < 2) {
		console.log("not enough emergency pepes...");
		if (!NProgress.isStarted())
			NProgress.start();
		return;
	}
	switch (pepe) {
		case "p1":
			var uuid = current_pepes[1];
			break;
		case "p2":
			var uuid = current_pepes[3];
			break;
	}
	next_pepes();
	setTimeout(function () {
		console.log("voting for", uuid);
		console.log("queue size:", pepe_queue.length);
		$("#votes").attr("data-votes", parseInt($("#votes").attr("data-votes")) + 1);
		$("#votes").text($("#votes").attr("data-votes") + " votes on record");

		$.post("/api/vote/"+uuid, {}, function (data) {
			process_pepes(data);
		});
	}, 0);
}

$.post("/api/get_pepes", {}, function (data) {
	process_pepes(data);
	next_pepes();
});

for (var i = 0; i < preload-1; i++) {
	$.post("/api/get_pepes", {}, process_pepes);
}
