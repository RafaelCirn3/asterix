import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { Property, PropertyImage, PropertyPayload, PropertyStatus } from '../../core/models/property.model';
import { AuthService } from '../../core/services/auth.service';
import { STATIC_URL } from '../../core/services/api-url';
import { PropertyService } from '../../core/services/property.service';

@Component({
  selector: 'app-property-form',
  imports: [
    MatButtonModule,
    MatCheckboxModule,
    MatIconModule,
    MatInputModule,
    MatSelectModule,
    ReactiveFormsModule,
    RouterLink,
  ],
  templateUrl: './property-form.html',
  styleUrl: './property-form.scss',
})
export class PropertyForm implements OnInit {
  private readonly fb = inject(FormBuilder);
  readonly property = signal<Property | null>(null);
  readonly previews = signal<string[]>([]);
  readonly selectedFiles = signal<File[]>([]);
  readonly editing = computed(() => Boolean(this.property()));

  readonly form = this.fb.group({
    nome: ['', Validators.required],
    preco: [null as number | null, Validators.min(1)],
    cidade: [''],
    bairro: [''],
    endereco: [''],
    tipo: [''],
    area: [null as number | null, Validators.min(1)],
    quartos: [null as number | null, Validators.min(0)],
    banheiros: [null as number | null, Validators.min(0)],
    garagem: [null as number | null, Validators.min(0)],
    descricao_curta: [''],
    descricao: [''],
    status: ['Disponivel' as PropertyStatus, Validators.required],
    destacado: [false],
  });

  constructor(
    private readonly route: ActivatedRoute,
    private readonly router: Router,
    private readonly service: PropertyService,
    readonly auth: AuthService,
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.service.get(id).subscribe((property) => {
        this.property.set(property);
        this.form.patchValue({
          ...property,
          preco: property.preco === null ? null : Number(property.preco),
        });
      });
    }
  }

  imageUrl(image: PropertyImage): string {
    return image.url ? `${STATIC_URL}${image.url}` : '';
  }

  onFilesSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const files = Array.from(input.files ?? []);
    this.selectedFiles.set(files);
    this.previews.set(files.map((file) => URL.createObjectURL(file)));
  }

  save(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const raw = this.form.getRawValue();
    const payload: PropertyPayload = {
      nome: raw.nome!.trim(),
      preco: raw.preco,
      cidade: this.optionalText(raw.cidade),
      bairro: this.optionalText(raw.bairro),
      endereco: this.optionalText(raw.endereco),
      tipo: this.optionalText(raw.tipo),
      area: raw.area,
      quartos: raw.quartos,
      banheiros: raw.banheiros,
      garagem: raw.garagem,
      descricao_curta: this.optionalText(raw.descricao_curta),
      descricao: this.optionalText(raw.descricao),
      status: raw.status as PropertyStatus,
      destacado: Boolean(raw.destacado),
    };

    const request = this.property()
      ? this.service.update(this.property()!.id, payload)
      : this.service.create(payload);

    request.subscribe((property) => {
      const files = this.selectedFiles();
      if (!files.length) {
        this.router.navigate(['/admin/imoveis']);
        return;
      }
      this.service.uploadImages(property.id, files).subscribe(() => this.router.navigate(['/admin/imoveis']));
    });
  }

  setMain(image: PropertyImage): void {
    const property = this.property();
    if (!property) {
      return;
    }
    this.service.updateImage(property.id, image.id, { principal: true }).subscribe(() => this.reload(property.id));
  }

  move(image: PropertyImage, direction: -1 | 1): void {
    const property = this.property();
    if (!property) {
      return;
    }
    this.service
      .updateImage(property.id, image.id, { ordem: Math.max(0, image.ordem + direction) })
      .subscribe(() => this.reload(property.id));
  }

  removeImage(image: PropertyImage): void {
    const property = this.property();
    if (!property || !confirm('Excluir esta imagem?')) {
      return;
    }
    this.service.deleteImage(property.id, image.id).subscribe(() => this.reload(property.id));
  }

  private optionalText(value: string | null): string | null {
    const normalized = value?.trim() ?? '';
    return normalized || null;
  }

  private reload(id: number): void {
    this.service.get(id).subscribe((property) => this.property.set(property));
  }
}
