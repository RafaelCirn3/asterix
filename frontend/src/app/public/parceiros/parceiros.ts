import {
  ChangeDetectionStrategy,
  Component,
  OnInit,
  signal,
} from '@angular/core';

import { CommonModule } from '@angular/common';

import { ParceirosCard } from '../parceiros-card/parceiros-card';
import { Partner } from '../../core/models/partner.model';

@Component({
  selector: 'app-parceiros',
  standalone: true,
  imports: [
    CommonModule,
    ParceirosCard,
  ],
  templateUrl: './parceiros.html',
  styleUrls: ['./parceiros.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Parceiros implements OnInit {

  readonly loading = signal(true);

  readonly partners = signal<Partner[]>([]);

  ngOnInit(): void {

    setTimeout(() => {

      // TODO: substituir por logos reais dos parceiros
      this.partners.set([

        {
          id: '1',
          nome: 'Parceiro 1',
          logoUrl: '/franq.jpeg'
        },


      ]);

      this.loading.set(false);

    }, 800);

  }

  trackByPartner(_: number, partner: Partner): string {

    return partner.id;

  }

}