function upload_weights(model_name, usb_head, lsb_head, usb_weigths, lsb_weigths, parallel)
    len = length(lsb_weigths);
    lsb_resize = reshape(lsb_weigths, [parallel, len/parallel]);
    usb_resize = reshape(usb_weigths, [parallel, len/parallel]);
    for i=[0:1:parallel-1]
        aux_lsb = lsb_resize(i+1, :);
        aux_usb = usb_resize(i+1, :);
        lsb_rom_re = strcat(model_name,'/',lsb_head, int2str(i),'/rom_re');
        lsb_rom_im = strcat(model_name,'/',lsb_head, int2str(i),'/rom_im');
        
        lsb_re = strcat('[', num2str(real(aux_lsb)), ']');
        lsb_im = strcat('[', num2str(imag(aux_lsb)), ']');
        set_param(lsb_rom_re, 'initVector', lsb_re);
        set_param(lsb_rom_im, 'initVector', lsb_im);
        
        usb_rom_re = strcat(model_name,'/',usb_head, int2str(i),'/rom_re');
        usb_rom_im = strcat(model_name,'/',usb_head, int2str(i),'/rom_im');
        usb_re = strcat('[', num2str(real(aux_usb)), ']');
        usb_im = strcat('[', num2str(imag(aux_usb)), ']');
        set_param(usb_rom_re, 'initVector', usb_re);
        set_param(usb_rom_im, 'initVector', usb_im);
    end
end