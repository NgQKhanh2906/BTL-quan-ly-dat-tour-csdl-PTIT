export const HERO_IMAGE = '/images/hero-northern-vietnam.jpg';
export const PROMO_CRUISE_IMAGE = '/images/promo-cruise.jpg';

export const TOUR_IMAGES: Record<string, string> = {
  T01: '/images/tour-T01.jpg',
  T02: '/images/tour-T02.jpg',
  T03: '/images/tour-T03.jpg',
  T04: '/images/tour-T04.jpg',
  T05: '/images/tour-T05.jpg',
  T06: '/images/tour-T06.jpg',
  T07: '/images/tour-T07.jpg',
  T08: '/images/tour-T08.jpg',
  T09: '/images/tour-T09.jpg',
};

export const TOUR_IMAGE_ALTS: Record<string, string> = {
  T01: 'Vịnh Hạ Long xanh trong và hoạt động chèo kayak giữa núi đá vôi',
  T02: 'Sa Pa, ruộng bậc thang và biển mây đỉnh Fansipan Lào Cai',
  T03: 'Thuyền nan xuôi dòng sông giữa núi đá vôi Tràng An, Ninh Bình',
  T04: 'Đồi chè xanh mướt trên cao nguyên Mộc Châu, Sơn La',
  T05: 'Đảo Cát Bà và mặt nước xanh ngọc Vịnh Lan Hạ, Hải Phòng',
  T06: 'Thác Bản Giốc hùng vĩ giữa núi non Cao Bằng',
  T07: 'Du thuyền cao cấp nghỉ đêm trên Vịnh Hạ Long và Lan Hạ',
  T08: 'Cung đường đèo núi Tây Bắc và thung lũng Mường Thanh, Điện Biên',
  T09: 'Đèo Mã Pì Lèng và dòng sông Nho Quế xanh biếc, Hà Giang',
};

export function getTourImage(maTour?: string | null): string {
  if (!maTour) return HERO_IMAGE;
  return TOUR_IMAGES[maTour.toUpperCase()] ?? HERO_IMAGE;
}

export function getTourImageAlt(maTour?: string | null, fallbackTitle?: string): string {
  if (maTour && TOUR_IMAGE_ALTS[maTour.toUpperCase()]) {
    return TOUR_IMAGE_ALTS[maTour.toUpperCase()];
  }
  return fallbackTitle || 'Phong cảnh du lịch miền Bắc Việt Nam';
}
