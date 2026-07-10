import { Routes } from '@angular/router';

import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./public/home/home').then((m) => m.Home),
  },
  {
    path: 'imoveis',
    loadComponent: () => import('./public/properties/properties').then((m: any) => m.Properties),
  },
  {
    path: 'imoveis/:id',
    loadComponent: () =>
      import('./public/property-detail/property-detail').then((m) => m.PropertyDetail),
  },
  {
    path: 'sobre',
    loadComponent: () => import('./public/about/about').then((m) => m.About),
  },
  {
    path: 'contato',
    loadComponent: () => import('./public/contact/contact').then((m) => m.Contact),
  },
  {
    path: 'admin/login',
    loadComponent: () => import('./admin/login/login').then((m) => m.Login),
  },
  {
    path: 'admin',
    canActivate: [authGuard],
    children: [
      {
        path: '',
        pathMatch: 'full',
        redirectTo: 'dashboard',
      },
      {
        path: 'dashboard',
        loadComponent: () => import('./admin/dashboard/dashboard').then((m) => m.Dashboard),
      },
      {
        path: 'imoveis',
        loadComponent: () =>
          import('./admin/properties-admin/properties-admin').then((m) => m.PropertiesAdmin),
      },
      {
        path: 'imoveis/novo',
        loadComponent: () =>
          import('./admin/property-form/property-form').then((m) => m.PropertyForm),
      },
      {
        path: 'imoveis/:id/editar',
        loadComponent: () =>
          import('./admin/property-form/property-form').then((m) => m.PropertyForm),
      },
    ],
  },
  { path: '**', redirectTo: '' },
];
