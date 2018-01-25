class ReactionTimeGame {
    constructor() {
        $('#reset').click(() => {
            $.getJSON('reset', {}, (data) => {
		location.reload(true);
	    }
        )});
        this.updateStatus(true);
    }

    updateStatus(noWait) {
        console.log('Fetching status');
        $.getJSON('status' + (noWait ? 'NoWait' : ''), {}, (data) => {
            console.log('Got status');
            $('#event').text(data.event || '');
            $('#scores tbody').empty();
            const scoresTbody = $('#scores tbody');
            for (let nameScore of data.scores) {
                scoresTbody.append(
                    `<tr><td>${nameScore[0]}</td><td>${nameScore[1]}</td><td>${nameScore[2]}</td><td>${nameScore[3]}</td><td>${nameScore[4]}</td></tr>`);
            }
            setTimeout(game.updateStatus, 100);
        });
    }
}

const game = new ReactionTimeGame();
