function makeSlider(id, when_changed) {
    // Dane wewnętrzne
    let touched = false;
    let changed = false;
    let position = 0;
    const slider = $('#' + id);
    // Funkcje wewnętrzne
    const set_position = function(new_position) {
        position = Math.round(new_position);
        slider.find('.slider_tick')[0].setAttribute('cy', position);
        changed = true;
    };
    slider.on('touchmove', event => {
        let touch = event.targetTouches[0];
        // Ustalenie miejsca dotknięcia względem górnej krawędzi suwaka
        let from_top = touch.pageY - slider.offset().top;
        // Zamiana na podwójną wartość procentową suwaka (0 to środek)
        let relative_touch = (from_top / slider.height()) * 200;
        set_position(relative_touch - 100);
        touched = true;
        event.preventDefault();
    });
    slider.on('touchend', () => touched = false);

    const update = function() {
        if(!touched && Math.abs(position) > 0) {
            // Powrót do środka - dodanie 0,5 do ruchu, by zaokrąglić przynajmniej do  1%
            let error = 0 - position;
            let change = (0.3 * error) + (Math.sign(error) * 0.5);
            set_position(position + change);
            // console.log(id + ": " + position);
        }
    };
    setInterval(update, 50);

    const update_if_changed = function() {
        if(changed) {
            changed = false;
            // Wywołanie zwrotne - odwrócenie suwaka, by dodatnie wartości były u góry
            when_changed(-position);
        }
    };
    setInterval(update_if_changed, 200);
}
