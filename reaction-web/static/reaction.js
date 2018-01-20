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
        console.log('Fetching status');
        $.getJSON('status', {}, (data) => {
            console.log('Got status');
            $('#event').text(data.event);
            $('#scores tbody').empty();
            const scoresTbody = $('#scores tbody');
            for (let nameScore of data.scores) {
                scoresTbody.append(
                    `<tr><td>${nameScore[0]}</td><td>${nameScore[1]}</td><td>${nameScore[2]}</td></tr>`);
            }
            setTimeout(game.updateStatus, 100);
        });
    }
}

const game = new ReactionTimeGame();
