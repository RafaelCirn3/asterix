import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
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
    MatSnackBarModule,
    ReactiveFormsModule,
    RouterLink,
  ],
  templateUrl: './property-form.html',
  styleUrl: './property-form.scss',
})
export class PropertyForm implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly snackBar = inject(MatSnackBar);
  readonly property = signal<Property | null>(null);
  readonly previews = signal<string[]>([]);
  readonly selectedFiles = signal<File[]>([]);
  readonly saving = signal(false);
  readonly editing = computed(() => Boolean(this.property()));

  readonly form = this.fb.group({
    nome: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(180)]],
    preco: [null as number | null, Validators.min(1)],
    cidade: [''],
    bairro: [''],
    endereco: [''],
    tipo: [''],
    area: [null as number | null, Validators.min(1)],
    quartos: [null as number | null, Validators.min(0)],
    banheiros: [null as number | null, Validators.min(0)],
    garagem: [null as number | null, Validators.min(0)],
    descricao_curta: ['', [Validators.minLength(10), Validators.maxLength(300)]],
    descricao: ['', Validators.minLength(20)],
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
      this.service.get(id).subscribe({
        next: (property) => {
          this.property.set(property);
          this.form.patchValue({
            ...property,
            preco: property.preco === null ? null : Number(property.preco),
          });
        },
        error: (error: HttpErrorResponse) => this.notifyError(error, 'Não foi possível carregar o imóvel.'),
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
    if (this.saving()) {
      return;
    }

    const trimmedName = this.form.controls.nome.value?.trim() ?? '';
    if (trimmedName.length < 3) {
      this.form.controls.nome.setErrors({ ...(this.form.controls.nome.errors ?? {}), trimmedMinLength: true });
    }

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.snackBar.open(
        'Revise os campos inválidos antes de salvar. Nome: mínimo 3 caracteres; descrição curta: mínimo 10; descrição completa: mínimo 20.',
        'Fechar',
        { duration: 7000 },
      );
      return;
    }

    const raw = this.form.getRawValue();
    const payload: PropertyPayload = {
      nome: trimmedName,
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

    this.saving.set(true);
    const isEditing = Boolean(this.property());
    const request = isEditing
      ? this.service.update(this.property()!.id, payload)
      : this.service.create(payload);

    request.subscribe({
      next: (property) => this.handleSavedProperty(property, isEditing),
      error: (error: HttpErrorResponse) => {
        this.saving.set(false);
        this.notifyError(error, isEditing ? 'Não foi possível atualizar o imóvel.' : 'Não foi possível criar o imóvel.');
      },
    });
  }

  setMain(image: PropertyImage): void {
    const property = this.property();
    if (!property) {
      return;
    }
    this.service.updateImage(property.id, image.id, { principal: true }).subscribe({
      next: () => this.reload(property.id),
      error: (error: HttpErrorResponse) => this.notifyError(error, 'Não foi possível alterar a imagem principal.'),
    });
  }

  move(image: PropertyImage, direction: -1 | 1): void {
    const property = this.property();
    if (!property) {
      return;
    }
    this.service
      .updateImage(property.id, image.id, { ordem: Math.max(0, image.ordem + direction) })
      .subscribe({
        next: () => this.reload(property.id),
        error: (error: HttpErrorResponse) => this.notifyError(error, 'Não foi possível reordenar a imagem.'),
      });
  }

  removeImage(image: PropertyImage): void {
    const property = this.property();
    if (!property || !confirm('Excluir esta imagem?')) {
      return;
    }
    this.service.deleteImage(property.id, image.id).subscribe({
      next: () => this.reload(property.id),
      error: (error: HttpErrorResponse) => this.notifyError(error, 'Não foi possível excluir a imagem.'),
    });
  }

  private handleSavedProperty(property: Property, wasEditing: boolean): void {
    this.property.set(property);
    const files = this.selectedFiles();

    if (!files.length) {
      this.saving.set(false);
      this.snackBar.open(wasEditing ? 'Imóvel atualizado com sucesso.' : 'Imóvel criado com sucesso.', 'Fechar', {
        duration: 3500,
      });
      this.router.navigate(['/admin/imoveis']);
      return;
    }

    this.service.uploadImages(property.id, files).subscribe({
      next: () => {
        this.saving.set(false);
        this.snackBar.open(wasEditing ? 'Imóvel e imagens atualizados com sucesso.' : 'Imóvel e imagens cadastrados com sucesso.', 'Fechar', {
          duration: 3500,
        });
        this.router.navigate(['/admin/imoveis']);
      },
      error: (error: HttpErrorResponse) => {
        this.saving.set(false);
        this.notifyError(
          error,
          'O imóvel foi salvo, mas o upload das imagens falhou. Abra o imóvel para tentar enviar as imagens novamente.',
          9000,
        );
        this.router.navigate(['/admin/imoveis', property.id, 'editar']);
      },
    });
  }

  private optionalText(value: string | null): string | null {
    const normalized = value?.trim() ?? '';
    return normalized || null;
  }

  private reload(id: number): void {
    this.service.get(id).subscribe({
      next: (property) => this.property.set(property),
      error: (error: HttpErrorResponse) => this.notifyError(error, 'Não foi possível atualizar os dados do imóvel.'),
    });
  }

  private notifyError(error: HttpErrorResponse, fallback: string, duration = 7000): void {
    let detail = '';

    if (error.status === 0) {
      detail = 'Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.';
    } else if (error.status === 401) {
      detail = 'Sua sessão expirou ou não é válida. Faça login novamente.';
    } else if (error.status === 403) {
      detail = 'Você não tem permissão para realizar esta operação.';
    } else if (error.status === 422) {
      detail = this.validationMessage(error) || 'Alguns dados enviados são inválidos. Revise o formulário.';
    } else if (error.status >= 500) {
      detail = 'O servidor encontrou um erro ao processar a solicitação. Tente novamente; se persistir, verifique os logs do backend.';
    } else if (typeof error.error?.detail === 'string' && error.error.detail.trim()) {
      detail = error.error.detail;
    }

    const message = detail ? `${fallback} ${detail}` : fallback;
    this.snackBar.open(message, 'Fechar', { duration });
  }

  private validationMessage(error: HttpErrorResponse): string | null {
    const detail = error.error?.detail;
    if (!Array.isArray(detail)) {
      return typeof detail === 'string' ? detail : null;
    }

    const messages = detail
      .map((item: any) => {
        const field = Array.isArray(item?.loc) ? item.loc[item.loc.length - 1] : null;
        const description = item?.msg;
        if (!description) {
          return null;
        }
        return field ? `${field}: ${description}` : description;
      })
      .filter(Boolean);

    return messages.length ? `Dados inválidos — ${messages.join('; ')}` : null;
  }
}
