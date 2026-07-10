import {
    Component,
    ElementRef,
    HostListener,
    ViewChild,
    signal
} from '@angular/core';

import {
    RouterLink,
    RouterLinkActive
} from '@angular/router';

@Component({
    selector: 'app-header-asterix',
    standalone: true,
    imports: [
        RouterLink,
        RouterLinkActive
    ],
    templateUrl: './header-asterix.html',
    styleUrl: './header-asterix.scss'
})
export class HeaderAsterix {

    // ============================================================
    // MENU MOBILE
    // ============================================================

    readonly menuOpen = signal(false);

    @ViewChild('menuDrawer')
    menuDrawer!: ElementRef<HTMLElement>;

    // ============================================================
    // MENU
    // ============================================================

    openMenu(): void {

        this.menuOpen.set(true);

        document.body.style.overflow = 'hidden';

        queueMicrotask(() => {

            this.menuDrawer
                ?.nativeElement
                ?.querySelector<HTMLAnchorElement>('a')
                ?.focus();

        });

    }

    closeMenu(): void {

        this.menuOpen.set(false);

        document.body.style.overflow = '';

    }

    toggleMenu(): void {

        this.menuOpen()
            ? this.closeMenu()
            : this.openMenu();

    }

    // ============================================================
    // ESC
    // ============================================================

    @HostListener('document:keydown.escape')

    onEscape(): void {

        if (this.menuOpen()) {

            this.closeMenu();

        }

    }

}