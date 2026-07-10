import {
    Component,
    signal
} from '@angular/core';

import {
    RouterLink
} from '@angular/router';


@Component({

    selector: 'app-footer-asterix',

    standalone: true,

    imports: [
        RouterLink
    ],

    templateUrl:
        './footer-asterix.html',

    styleUrl:
        './footer-asterix.scss'

})

export class FooterAsterix {


    // ============================================================
    // ANO DINÂMICO
    // ============================================================

    readonly currentYear = signal(
        new Date().getFullYear()
    );


}