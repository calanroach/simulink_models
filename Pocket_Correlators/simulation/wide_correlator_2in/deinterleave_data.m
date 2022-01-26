function dout= deinterleave_data(din, channels)
    [ndata, streams] = size(din);
    n_spectra = floor(ndata*streams/(channels));
    dout = reshape(din(1:n_spectra*channels/streams,:)', [channels,n_spectra]);
end