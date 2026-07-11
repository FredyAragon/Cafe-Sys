import { Injectable, signal, computed } from '@angular/core';
import { Producto } from './api';

export interface CartItem {
  product: Producto;
  quantity: number;
}

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private _items = signal<CartItem[]>([]);

  readonly items = computed(() => this._items());
  readonly count = computed(() => this._items().reduce((sum, item) => sum + item.quantity, 0));
  readonly total = computed(() =>
    this._items().reduce((sum, item) => sum + Number(item.product.price) * item.quantity, 0)
  );

  addProduct(product: Producto, quantity = 1): void {
    this._items.update(items => {
      const existing = items.find(item => item.product.id === product.id);
      if (existing) {
        return items.map(item =>
          item.product.id === product.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        );
      }
      return [...items, { product, quantity }];
    });
  }

  removeProduct(productId: number): void {
    this._items.update(items => items.filter(item => item.product.id !== productId));
  }

  updateQuantity(productId: number, quantity: number): void {
    if (quantity <= 0) {
      this.removeProduct(productId);
      return;
    }
    this._items.update(items =>
      items.map(item =>
        item.product.id === productId ? { ...item, quantity } : item
      )
    );
  }

  clear(): void {
    this._items.set([]);
  }
}
