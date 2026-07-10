import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderAsterix } from './shared/components/header-asterix/header-asterix';
import { FooterAsterix } from './shared/components/footer-asterix/footer-asterix';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HeaderAsterix, FooterAsterix],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('Asterix Consultoria Imobiliaria');

}
