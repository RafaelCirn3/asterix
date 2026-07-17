import { Component, Input } from '@angular/core';
import { Partner } from '../../core/models/partner.model';

@Component({
  selector: 'app-parceiros-card',
  standalone: true,
  imports: [],
  templateUrl: './parceiros-card.html',
  styleUrls: ['./parceiros-card.scss'],
})
export class ParceirosCard {

  @Input({ required: true })
  partner!: Partner;

}