class ReactionTimeGame {
    constructor() {
        $('#reset').click(() => {
            $.getJSON('reset', {}, (data) => {
		location.reload(true);
	    }
        )});
        this.updateStatus();
    }

    updateStatus() {
        console.log('us');
        $.getJSON('status', {}, (data) => {
            console.log(data);
            $('#event').text(data.event);
            $('#scores tbody').empty();
            const scoresTbody = $('#scores tbody');
            for (let nameScore of data.scores) {
                console.log(nameScore);
                scoresTbody.append(`<tr><td>${nameScore[0]}</td><td>${nameScore[1]}</td></tr>`);
            }
            setTimeout(game.updateStatus, 100);
        });
    }
}

const game = new ReactionTimeGame();
